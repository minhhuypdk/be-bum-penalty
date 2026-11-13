// Original synthesized music/effects; all audio waits for an explicit user gesture.
const button=document.getElementById('sound');
const volume=document.getElementById('sound-volume');
let context,master,enabled=false,timer=null,beat=0,lastEvent='',noise;
const Audio=window.AudioContext||window.webkitAudioContext;
const melody=[261.63,329.63,392,440,392,329.63,293.66,392];
function tone(frequency,duration=.15,gain=.12,type='sine') {
 if(!enabled||context.state!=='running')return;
 const oscillator=context.createOscillator(),envelope=context.createGain(),now=context.currentTime;
 oscillator.type=type;oscillator.frequency.value=frequency;envelope.gain.setValueAtTime(.001,now);envelope.gain.exponentialRampToValueAtTime(gain,now+.015);envelope.gain.exponentialRampToValueAtTime(.001,now+duration);
 oscillator.connect(envelope);envelope.connect(master);oscillator.start();oscillator.stop(now+duration+.02);
 oscillator.onended=()=>{oscillator.disconnect();envelope.disconnect()};
}
function cheer(duration=.8) {
 if(!enabled||context.state!=='running')return;
 const source=context.createBufferSource(),filter=context.createBiquadFilter(),gain=context.createGain(),now=context.currentTime;
 source.buffer=noise;filter.type='bandpass';filter.frequency.value=900;filter.Q.value=.6;
 gain.gain.setValueAtTime(.001,now);gain.gain.linearRampToValueAtTime(.12,now+.08);gain.gain.exponentialRampToValueAtTime(.001,now+duration);
 source.connect(filter);filter.connect(gain);gain.connect(master);source.start();source.stop(now+duration);source.onended=()=>{source.disconnect();filter.disconnect();gain.disconnect()};
}
function callName(person) {
 if(!enabled||!window.speechSynthesis)return;
 const voice=speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().startsWith('vi'));
 if(!voice)return; // Device voices vary; never substitute an unrelated language.
 speechSynthesis.cancel();const phrase=new SpeechSynthesisUtterance((person==='ba'?'Ba':'Bum')+' ơi, cố lên!');
 phrase.voice=voice;phrase.lang='vi-VN';phrase.rate=1.05;phrase.volume=Number(volume.value)/100;
 speechSynthesis.speak(phrase);
}
function paint(){button.textContent=enabled?'🔊 Âm thanh: bật':'🔇 Âm thanh: tắt';button.setAttribute('aria-pressed',String(enabled));button.dataset.audioState=enabled?'on':'off'}
button.addEventListener('click',async()=>{
 if(button.disabled)return;
 if(!Audio){button.textContent='Thiết bị chưa hỗ trợ âm thanh';button.disabled=true;return}
 button.disabled=true;
 try {
  if(!context){context=new Audio();master=context.createGain();master.gain.value=Number(volume.value)/100;master.connect(context.destination);
   noise=context.createBuffer(1,context.sampleRate,context.sampleRate);const samples=noise.getChannelData(0);let seed=17;
   for(let i=0;i<samples.length;i++){seed=(seed*16807)%2147483647;samples[i]=(seed/2147483647)*2-1;}
  }
  enabled=!enabled;
  if(enabled){await context.resume();tone(523,.15);timer=setInterval(()=>{if(document.hidden||context.state!=='running')return;tone(melody[beat%melody.length],.22,.055,'triangle');if(beat%2===0)tone(130.81,.16,.045);beat++;},350)}
  else{clearInterval(timer);timer=null;window.speechSynthesis?.cancel();await context.suspend()}
  paint();
 }catch(error){enabled=false;clearInterval(timer);timer=null;paint();console.warn('Không khởi tạo được âm thanh.',error)}finally{button.disabled=false}
});
volume.addEventListener('input',()=>{if(master)master.gain.setTargetAtTime(Number(volume.value)/100,context.currentTime,.05);if(volume.value==='0')window.speechSynthesis?.cancel()});
window.addEventListener('penalty:state',({detail:s})=>{
 const key=`${s.matchId}:${s.turn}:${s.stage}`;if(!enabled||key===lastEvent)return;lastEvent=key;
 if(s.stage==='result'){tone(100,.08,.18);cheer(s.shot!==s.dive?1.1:.65);if(s.shot!==s.dive){tone(523,.25,.15);setTimeout(()=>tone(659,.3,.13),140)}}
 if(s.stage==='choose'&&s.players?.ba&&s.players?.bum)callName(s.turn%2?'bum':'ba');
 if(s.stage==='finished'){cheer(1.2);callName(s.winner)}
});
document.addEventListener('visibilitychange',()=>{if(!context||!enabled)return;if(document.hidden){context.suspend();window.speechSynthesis?.cancel()}else context.resume().catch(()=>{})});
paint();
