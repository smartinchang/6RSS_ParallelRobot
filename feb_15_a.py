# Khai báo các thư viện
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

# Vị trí tâm của tấm dịch chuyển theo hệ tọa độ gắn trên bệ cố định
pb0=[0,0,0.13]

# Các góc quay của tấm dịch chuyển
ax=np.pi/24
ay=np.pi/24
az=np.pi/24
#az=np.pi/24

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
print("l1 =",l1)
print("l2 =",l2)
print("l3 =",l3)
print("l4 =",l4)
print("l5 =",l5)
print("l6 =",l6)

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
    d1=(0,0,1)
    d2=bb1
    p1=bb1
    p2=pb1
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp1=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    # Xác định góc quay của khớp chủ động trên chuỗi động thứ 2
    d1=(0,0,1)
    d2=bb2
    p1=bb2
    p2=pb2
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp2=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    # Xác định góc quay của khớp chủ động trên chuỗi động thứ 3
    d1=(0,0,1)
    d2=bb3
    p1=bb3
    p2=pb3
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp3=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    # Xác định góc quay của khớp chủ động trên chuỗi động thứ 4
    d1=(0,0,1)
    d2=bb4
    p1=bb4
    p2=pb4
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp4=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    # Xác định góc quay của khớp chủ động trên chuỗi động thứ 5
    d1=(0,0,1)
    d2=bb5
    p1=bb5
    p2=pb5
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp5=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    # Xác định góc quay của khớp chủ động trên chuỗi động thứ 6
    d1=(0,0,1)
    d2=bb6
    p1=bb6
    p2=pb6
    n=(d1[1]*d2[2]-d1[2]*d2[1],d1[2]*d2[0]-d1[0]*d2[2],d1[0]*d2[1]-d1[1]*d2[0])
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
    asp6=math.acos(nz[0]*nu[0]+nz[1]*nu[1]+nz[2]*nu[2]/(np.sqrt(nz[0]*nz[0]+nz[1]*nz[1]+nz[2]*nz[2])*np.sqrt(nu[0]*nu[0]+nu[1]*nu[1]+nu[2]*nu[2])))

    print("a1 =",a1*180/np.pi)
    print("a2 =",a2*180/np.pi)
    print("a3 =",a3*180/np.pi)
    print("a4 =",a4*180/np.pi)
    print("a5 =",a5*180/np.pi)
    print("a6 =",a6*180/np.pi)
    print("asp1 =",asp1*180/np.pi)
    print("asp2 =",asp2*180/np.pi)
    print("asp3 =",asp3*180/np.pi)
    print("asp4 =",asp4*180/np.pi)
    print("asp5 =",asp5*180/np.pi)
    print("asp6 =",asp6*180/np.pi)

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

    if (check>0):
        # Thiết lập chế độ vẽ
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim3d(-0.15,0.15)
        ax.set_ylim3d(-0.15,0.15)
        ax.set_zlim3d(0,0.3)

        # Vẽ các chuỗi động
        ax.plot3D([c1[0],pb1[0]],[c1[1],pb1[1]],[c1[2],pb1[2]])
        ax.plot3D([bb1[0],c1[0]],[bb1[1],c1[1]],[bb1[2],c1[2]])
        ax.plot3D([c2[0],pb2[0]],[c2[1],pb2[1]],[c2[2],pb2[2]])
        ax.plot3D([bb2[0],c2[0]],[bb2[1],c2[1]],[bb2[2],c2[2]])
        ax.plot3D([c3[0],pb3[0]],[c3[1],pb3[1]],[c3[2],pb3[2]])
        ax.plot3D([bb3[0],c3[0]],[bb3[1],c3[1]],[bb3[2],c3[2]])
        ax.plot3D([c4[0],pb4[0]],[c4[1],pb4[1]],[c4[2],pb4[2]])
        ax.plot3D([bb4[0],c4[0]],[bb4[1],c4[1]],[bb4[2],c4[2]])
        ax.plot3D([c5[0],pb5[0]],[c5[1],pb5[1]],[c5[2],pb5[2]])
        ax.plot3D([bb5[0],c5[0]],[bb5[1],c5[1]],[bb5[2],c5[2]])
        ax.plot3D([c6[0],pb6[0]],[c6[1],pb6[1]],[c6[2],pb6[2]])
        ax.plot3D([bb6[0],c6[0]],[bb6[1],c6[1]],[bb6[2],c6[2]])
        ax.plot3D(c1[0],c1[1],c1[2],".")
        ax.plot3D(c2[0],c2[1],c2[2],".")
        ax.plot3D(c3[0],c3[1],c3[2],".")
        ax.plot3D(c4[0],c4[1],c4[2],".")
        ax.plot3D(c5[0],c5[1],c5[2],".")
        ax.plot3D(c6[0],c6[1],c6[2],".")

        # Vẽ các điểm nối trên bệ cố định
        ax.plot3D([0,bb1[0]],[0,bb1[1]],[0,bb1[2]],"--")
        ax.plot3D([0,bb2[0]],[0,bb2[1]],[0,bb2[2]],"--")
        ax.plot3D([0,bb3[0]],[0,bb3[1]],[0,bb3[2]],"--")
        ax.plot3D([0,bb4[0]],[0,bb4[1]],[0,bb4[2]],"--")
        ax.plot3D([0,bb5[0]],[0,bb5[1]],[0,bb5[2]],"--")
        ax.plot3D([0,bb6[0]],[0,bb6[1]],[0,bb6[2]],"--")
        ax.plot3D(bb1[0],bb1[1],bb1[2],"o")
        ax.plot3D(bb2[0],bb2[1],bb2[2],"o")
        ax.plot3D(bb3[0],bb3[1],bb3[2],"o")
        ax.plot3D(bb4[0],bb4[1],bb4[2],"o")
        ax.plot3D(bb5[0],bb5[1],bb5[2],"o")
        ax.plot3D(bb6[0],bb6[1],bb6[2],"o")

        # Vẽ các điểm nối trên tấm dịch chuyển
        ax.plot3D([pb0[0],pb1[0]],[pb0[1],pb1[1]],[pb0[2],pb1[2]],"--")
        ax.plot3D([pb0[0],pb2[0]],[pb0[1],pb2[1]],[pb0[2],pb2[2]],"--")
        ax.plot3D([pb0[0],pb3[0]],[pb0[1],pb3[1]],[pb0[2],pb3[2]],"--")
        ax.plot3D([pb0[0],pb4[0]],[pb0[1],pb4[1]],[pb0[2],pb4[2]],"--")
        ax.plot3D([pb0[0],pb5[0]],[pb0[1],pb5[1]],[pb0[2],pb5[2]],"--")
        ax.plot3D([pb0[0],pb6[0]],[pb0[1],pb6[1]],[pb0[2],pb6[2]],"--")
        ax.plot3D([pb1[0],pb2[0]],[pb1[1],pb2[1]],[pb1[2],pb2[2]])
        ax.plot3D([pb2[0],pb3[0]],[pb2[1],pb3[1]],[pb2[2],pb3[2]])
        ax.plot3D([pb3[0],pb4[0]],[pb3[1],pb4[1]],[pb3[2],pb4[2]])
        ax.plot3D([pb4[0],pb5[0]],[pb4[1],pb5[1]],[pb4[2],pb5[2]])
        ax.plot3D([pb5[0],pb6[0]],[pb5[1],pb6[1]],[pb5[2],pb6[2]])
        ax.plot3D([pb6[0],pb1[0]],[pb6[1],pb1[1]],[pb6[2],pb1[2]])
        ax.plot3D(pb1[0],pb1[1],pb1[2],".")
        ax.plot3D(pb2[0],pb2[1],pb2[2],".")
        ax.plot3D(pb3[0],pb3[1],pb3[2],".")
        ax.plot3D(pb4[0],pb4[1],pb4[2],".")
        ax.plot3D(pb5[0],pb5[1],pb5[2],".")
        ax.plot3D(pb6[0],pb6[1],pb6[2],".")

        # Hiển thị hình ảnh
        plt.title("Robot song song 6-RSS")
        plt.show()
if (check==0):
    print("Vị trí và góc hướng này không nằm trong vùng làm việc của robot!")
