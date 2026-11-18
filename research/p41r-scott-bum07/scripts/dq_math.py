"""Independent mathematical DQS reference (Python, not Blender source code).
Normalized quaternion blending with hemisphere alignment; affine scale residual
around the bind bone. Based on the dual-quaternion skinning method of Kavan et al.
No third-party implementation copied. Used to TEST native Preserve Volume.
"""
from mathutils import Matrix,Quaternion,Vector

def bone_parts(pose,bind):
    # A bone's length axis is local Y. Preserve it when removing shear/scale.
    y=pose.col[1].to_3d().normalized()
    x=pose.col[0].to_3d();x=(x-y*x.dot(y)).normalized()
    z=x.cross(y).normalized();x=y.cross(z).normalized()
    rigid=Matrix.Identity(4)
    for i,a in enumerate([x,y,z]):
        for k in range(3):rigid[k][i]=a[k]
    rigid.translation=pose.translation
    diff=rigid@bind.inverted()
    q=diff.to_quaternion().normalized();t=diff.translation
    dual=(Quaternion((0,*t))@q)*.5
    residual=bind@rigid.inverted()@pose@bind.inverted()
    return q,dual,residual

def blended_matrix(parts,weights):
    q=Vector((0.,0.,0.,0.));d=q.copy();S=Matrix(((0.,)*4,)*4)
    for name,w in weights:
        qi,di,si=parts[name];a=Vector(tuple(qi));sign=-1 if q.dot(a)<0 else 1
        q+=a*(w*sign);d+=Vector(tuple(di))*(w*sign)
        for row in range(4):
            for col in range(4):S[row][col]+=w*si[row][col]
    length=q.length;assert length>1e-8
    qq=Quaternion(tuple(q/length));dd=Quaternion(tuple(d/length))
    T=qq.to_matrix().to_4x4();tr=dd@qq.conjugated();T.translation=Vector((tr.x,tr.y,tr.z))*2
    return T@S
