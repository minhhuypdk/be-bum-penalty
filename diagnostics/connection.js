const output=document.getElementById('report'),status=document.getElementById('status'),button=document.getElementById('run'),copy=document.getElementById('copy');
const digest=async text=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),n=>n.toString(16).padStart(2,'0')).join('');
function claims(token){try{const part=token.split('.')[1].replace(/-/g,'+').replace(/_/g,'/');return JSON.parse(atob(part.padEnd(Math.ceil(part.length/4)*4,'=')))}catch{return null}}
function safeError(error){
 const result={};
 for(const key of ['code','message','details','hint'])if(error?.[key]!=null)result[key]=String(error[key]).replace(/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,'[JWT redacted]');
 return result;
}
async function request(url,key,credential,label){
 const endpoint=new URL('/rest/v1/bebum_penalty_rooms',url);endpoint.searchParams.set('select','*');endpoint.searchParams.set('room_id','eq.ba-bum');
 const declared=credential?.split('.').length===3?claims(credential):null;
 const report={label,method:'GET',table:'public.bebum_penalty_rooms',credentialKind:credential===key?'publishable key':'stored token',declaredJwtRole:declared?.role??null,expiredJwt:declared?.exp?declared.exp*1000<Date.now():null};
 try{
  const response=await fetch(endpoint,{method:'GET',headers:{apikey:key,Authorization:`Bearer ${credential}`,'Accept-Profile':'public',Accept:'application/json'},cache:'no-store',signal:AbortSignal.timeout(15000)});
  const body=await response.json();report.httpStatus=response.status;report.requestId=response.headers.get('sb-request-id');
  if(response.ok)report.rowCount=Array.isArray(body)?body.length:null;
  else report.error=safeError(body);
 }catch(error){report.networkError=error.name+': '+error.message}
 return report;
}
async function run(){
 button.disabled=true;copy.disabled=true;status.textContent='Đang kiểm tra chỉ đọc…';
 try{
  const response=await fetch('./index.html',{cache:'no-store',signal:AbortSignal.timeout(15000)});if(!response.ok)throw new Error(`index.html: HTTP ${response.status}`);
  const html=await response.text(),url=html.match(/(?:SUPABASE_URL|URL)='([^']+)'/)?.[1],key=html.match(/KEY='([^']+)'/)?.[1];
  if(!url||!key||!key.startsWith('sb_publishable_'))throw new Error('Không tìm được URL/publishable key trong HTML đang phục vụ.');
  const parsed=new URL(url);if(parsed.protocol!=='https:'||!parsed.hostname.endsWith('.supabase.co'))throw new Error('URL dự án không hợp lệ.');
  const project=parsed.hostname.split('.')[0],storageKey=`sb-${project}-auth-token`;
  let token=null,storageReadable=true;
  try{const stored=JSON.parse(localStorage.getItem(storageKey)||'null');token=typeof stored?.access_token==='string'?stored.access_token:null}catch{storageReadable=false}
  const report={checkedAt:new Date().toISOString(),pageOrigin:location.origin,pagePath:location.pathname,projectURL:url,projectRef:project,indexSha256:await digest(html),gameUsesIsolatedAuth:html.includes('persistSession:false'),keyType:'publishable',keySuffix:key.slice(-6),keySha256:await digest(key),storageReadable,hasStoredAccessToken:!!token,requests:[],note:'JWT role chỉ là claim khai báo. Vai PostgreSQL/RLS cần đối chiếu SQL audit; kết quả anon thành công không chứng minh mọi role có quyền.'};
  report.requests.push(await request(url,key,key,'Control: publishable key, không dùng phiên lưu sẵn'));
  if(token)report.requests.push(await request(url,key,token,'Đối chứng token lưu sẵn, không phải request game khi isolatedAuth=true'));
  output.textContent=JSON.stringify(report,null,2);copy.disabled=false;
  const errors=report.requests.some(r=>r.networkError||r.httpStatus>=400);
  status.textContent=errors?'Đã ghi nhận lỗi. Hãy sao chép báo cáo để đối chiếu.':'Các request kiểm tra hiện thành công. Nếu game vẫn lỗi, hãy gửi báo cáo này.';
 }catch(error){output.textContent=JSON.stringify({error:error.message},null,2);status.textContent='Chưa hoàn tất kiểm tra.'}
 finally{button.disabled=false}
}
button.addEventListener('click',run);
copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(output.textContent);status.textContent='Đã sao chép báo cáo, không có token bí mật.'}catch{status.textContent='Không sao chép tự động được; hãy chọn nội dung báo cáo bên dưới.'}});
run();
