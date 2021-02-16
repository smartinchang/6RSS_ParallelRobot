# Khai báo các thư viện
import numpy as np
import math

# Hàm thực hiện phép biến đổi theo các góc quay và tịnh tiến
def transform(p0,ax,ay,az,pt):
    # Các tham số của ma trận quay
    xc=np.cos(ax)
    xs=np.sin(ax)
    yc=np.cos(ay)
    ys=np.sin(ay)
    zc=np.cos(az)
    zs=np.sin(az)
    r11=zc*yc
    r12=zc*ys*xs-zs*xc
    r13=zc*ys*xc+zs*xs
    r21=zs*yc
    r22=zs*ys*xs+zc*xc
    r23=zs*ys*xs-zc*xs
    r31=-ys
    r32=zc*xs
    r33=yc*xc
    # Tính tọa độ của điểm được biến đổi
    p=(r11*p0[0]+r12*p0[1]+r13*p0[2]+pt[0],r21*p0[0]+r22*p0[1]+r23*p0[2]+pt[1],r31*p0[0]+r32*p0[1]+r33*p0[2]+pt[2])
    return p

# Hàm xác định chiều dài giữa 2 điểm
def length(p1,p2):
    l=np.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])+(p1[2]-p2[2])*(p1[2]-p2[2]))
    return l

# Hàm xác định góc giữa 2 vector
def angle2vector(a,b):
    angle=math.acos((a[0]*b[0]+a[1]*b[1]+a[2]*b[2])/(np.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])*np.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])))
    return angle

# Hàm tích có hướng cùa 2 vector
def cross(a,b):
    n=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    return n

# Các thông số của robot
lu=0.1
ll=0.05
lsa=np.pi/4

# Các thông số của tấm dịch chuyển
rp=0.1

# Tính tọa độ các điểm nối trên tấm dịch chuyển
pp1=[rp*np.cos(0*np.pi/3),rp*np.sin(0*np.pi/3),0]
pp2=[rp*np.cos(1*np.pi/3),rp*np.sin(1*np.pi/3),0]
pp3=[rp*np.cos(2*np.pi/3),rp*np.sin(2*np.pi/3),0]
pp4=[rp*np.cos(3*np.pi/3),rp*np.sin(3*np.pi/3),0]
pp5=[rp*np.cos(4*np.pi/3),rp*np.sin(4*np.pi/3),0]
pp6=[rp*np.cos(5*np.pi/3),rp*np.sin(5*np.pi/3),0]

# Các thông số của bệ cố định
rb=0.1

# Tính tọa độ các điểm nối trên bệ cố định
bb1=[rb*np.cos(0*np.pi/3),rb*np.sin(0*np.pi/3),0]
bb2=[rb*np.cos(1*np.pi/3),rb*np.sin(1*np.pi/3),0]
bb3=[rb*np.cos(2*np.pi/3),rb*np.sin(2*np.pi/3),0]
bb4=[rb*np.cos(3*np.pi/3),rb*np.sin(3*np.pi/3),0]
bb5=[rb*np.cos(4*np.pi/3),rb*np.sin(4*np.pi/3),0]
bb6=[rb*np.cos(5*np.pi/3),rb*np.sin(5*np.pi/3),0]

# Tính các góc quay của các điểm nối trên bệ cố định
ab1=0*np.pi/3
ab2=1*np.pi/3
ab3=2*np.pi/3
ab4=3*np.pi/3
ab5=4*np.pi/3
ab6=5*np.pi/3

# Hàm kiểm tra vị trí và góc hướng có thuộc vùng làm việc hay không
def workspace(pb0,ax,ay,az):
    # Tính vector pháp tuyến của tấm dịch chuyển
    nz=transform((0,0,0.1),ax,ay,az,(0,0,0))

    # Tính tọa độ các điểm nối trên tấm dịch chuyển theo hệ tọa độ gắn trên bệ cố định
    pb1=transform(pp1,ax,ay,az,pb0)
    pb2=transform(pp2,ax,ay,az,pb0)
    pb3=transform(pp3,ax,ay,az,pb0)
    pb4=transform(pp4,ax,ay,az,pb0)
    pb5=transform(pp5,ax,ay,az,pb0)
    pb6=transform(pp6,ax,ay,az,pb0)

    # Xác định chiều dài giới hạn của các chuỗi động
    l1=length(pb1,bb1)
    l2=length(pb2,bb2)
    l3=length(pb3,bb3)
    l4=length(pb4,bb4)
    l5=length(pb5,bb5)
    l6=length(pb6,bb6)

    # Kiểm tra các giới hạn về chiều dài của các chuỗi động
    check=1
    if (l1>(lu+ll)) or (lu>(l1+ll)) or (ll>(l1+lu)):
        check=0
    if (l2>(lu+ll)) or (lu>(l2+ll)) or (ll>(l2+lu)):
        check=0
    if (l3>(lu+ll)) or (lu>(l3+ll)) or (ll>(l3+lu)):
        check=0
    if (l4>(lu+ll)) or (lu>(l4+ll)) or (ll>(l4+lu)):
        check=0
    if (l5>(lu+ll)) or (lu>(l5+ll)) or (ll>(l5+lu)):
        check=0
    if (l6>(lu+ll)) or (lu>(l6+ll)) or (ll>(l6+lu)):
        check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 1
        d1=(0,0,-1)
        d2=bb1
        p1=bb1
        p2=pb1
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a1=aa+ab
        c1=transform((-ll,0,0),0,a1,ab1,bb1)
        nu=(pb1[0]-c1[0],pb1[1]-c1[1],pb1[2]-c1[2])
        asp1=angle2vector(nz,nu)
        nl=(c1[0]-bb1[0],c1[1]-bb1[1],c1[2]-bb1[2])
        zl=cross(n,nl)
        asb1=angle2vector(nu,zl)

        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 2
        d2=bb2
        p1=bb2
        p2=pb2
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a2=aa+ab
        c2=transform((-ll,0,0),0,a2,ab2,bb2)
        nu=(pb2[0]-c2[0],pb2[1]-c2[1],pb2[2]-c2[2])
        asp2=angle2vector(nz,nu)
        nl=(c2[0]-bb2[0],c2[1]-bb2[1],c2[2]-bb2[2])
        zl=cross(n,nl)
        asb2=angle2vector(nu,zl)

        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 3
        d2=bb3
        p1=bb3
        p2=pb3
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a3=aa+ab
        c3=transform((-ll,0,0),0,a3,ab3,bb3)
        nu=(pb3[0]-c3[0],pb3[1]-c3[1],pb3[2]-c3[2])
        asp3=angle2vector(nz,nu)
        nl=(c3[0]-bb3[0],c3[1]-bb3[1],c3[2]-bb3[2])
        zl=cross(n,nl)
        asb3=angle2vector(nu,zl)

        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 4
        d2=bb4
        p1=bb4
        p2=pb4
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a4=aa+ab
        c4=transform((-ll,0,0),0,a4,ab4,bb4)
        nu=(pb4[0]-c4[0],pb4[1]-c4[1],pb4[2]-c4[2])
        asp4=angle2vector(nz,nu)
        nl=(c4[0]-bb4[0],c4[1]-bb4[1],c4[2]-bb4[2])
        zl=cross(n,nl)
        asb4=angle2vector(nu,zl)

        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 5
        d2=bb5
        p1=bb5
        p2=pb5
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a5=aa+ab
        c5=transform((-ll,0,0),0,a5,ab5,bb5)
        nu=(pb5[0]-c5[0],pb5[1]-c5[1],pb5[2]-c5[2])
        asp5=angle2vector(nz,nu)
        nl=(c5[0]-bb5[0],c5[1]-bb5[1],c5[2]-bb5[2])
        zl=cross(n,nl)
        asb5=angle2vector(nu,zl)

        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 6
        d2=bb6
        p1=bb6
        p2=pb6
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        lb=np.sqrt(lu*lu-la*la)
        lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
        ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
        aa=math.acos((rb*rb+lc*lc-ld*ld)/(2*rb*lc))
        ab=math.acos((lc*lc+ll*ll-lb*lb)/(2*lc*ll))
        a6=aa+ab
        c6=transform((-ll,0,0),0,a6,ab6,bb6)
        nu=(pb6[0]-c6[0],pb6[1]-c6[1],pb6[2]-c6[2])
        asp6=angle2vector(nz,nu)
        nl=(c6[0]-bb6[0],c6[1]-bb6[1],c6[2]-bb6[2])
        zl=cross(n,nl)
        asb6=angle2vector(nu,zl)

        # Kiểm tra giới hạn các góc quay
        if (a1<0) or (a1>np.pi):
            check=0
        if (a2<0) or (a2>np.pi):
            check=0
        if (a3<0) or (a3>np.pi):
            check=0
        if (a4<0) or (a4>np.pi):
            check=0
        if (a5<0) or (a5>np.pi):
            check=0
        if (a6<0) or (a6>np.pi):
            check=0
        if (abs(asp1)>lsa):
            check=0
        if (abs(asp2)>lsa):
            check=0
        if (abs(asp3)>lsa):
            check=0
        if (abs(asp4)>lsa):
            check=0
        if (abs(asp5)>lsa):
            check=0
        if (abs(asp6)>lsa):
            check=0
        if (abs(asb1)>lsa):
            check=0
        if (abs(asb2)>lsa):
            check=0
        if (abs(asb3)>lsa):
            check=0
        if (abs(asb4)>lsa):
            check=0
        if (abs(asb5)>lsa):
            check=0
        if (abs(asb6)>lsa):
            check=0
    return check

# Vị trí tâm của tấm dịch chuyển theo hệ tọa độ gắn trên bệ cố định
pb0=[0,0,0.11]

# Các góc quay của tấm dịch chuyển
ax=np.pi/24
ay=np.pi/24
az=np.pi/24

# Kiểm tra vị trí và góc hướng có thuộc vùng làm việc hay không
if (workspace(pb0,ax,ay,az)==1):
    print("Vị trí và góc hướng thuộc vùng làm việc")
else:
    print("Vị trí và góc hướng không thuộc vùng làm việc")
