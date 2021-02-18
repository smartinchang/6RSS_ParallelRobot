# Khai báo các thư viện
from tkinter import *
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

# Hàm xác định góc giữa 2 vector
def angle2vector(a,b):
    angle=math.acos((a[0]*b[0]+a[1]*b[1]+a[2]*b[2])/(np.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])*np.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])))
    return angle

# Hàm tích có hướng cùa 2 vector
def cross(a,b):
    n=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    return n

# Hàm kiểm tra vị trí và góc hướng có thuộc vùng làm việc hay không
def checkin(pb0,ax,ay,az):
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
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if (abs(round((lc*lc+ll*ll-lb*lb),8))<=abs(round((2*lc*ll),8))) and (round((lc*lc+ll*ll-lb*lb),8))<=abs(round((2*lc*ll),8)) and ((rb*lc)!=0) and ((lc*ll)!=0):
            #if (((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2))):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld),8)/round((2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb),8)/round((2*lc*ll),8))
                a1=aa+ab
                c1=transform((-ll,0,0),0,a1,ab1,bb1)
                nu=(pb1[0]-c1[0],pb1[1]-c1[1],pb1[2]-c1[2])
                asp1=angle2vector(nz,nu)
                nl=(c1[0]-bb1[0],c1[1]-bb1[1],c1[2]-bb1[2])
                zl=cross(n,nl)
                asb1=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 2
        d2=bb2
        p1=bb2
        p2=pb2
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if ((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2)):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld),8)/round((2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb),8)/round((2*lc*ll),8))
                a2=aa+ab
                c2=transform((-ll,0,0),0,a2,ab2,bb2)
                nu=(pb2[0]-c2[0],pb2[1]-c2[1],pb2[2]-c2[2])
                asp2=angle2vector(nz,nu)
                nl=(c2[0]-bb2[0],c2[1]-bb2[1],c2[2]-bb2[2])
                zl=cross(n,nl)
                asb2=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 3
        d2=bb3
        p1=bb3
        p2=pb3
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if ((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2)):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld),8)/round((2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb),8)/round((2*lc*ll),8))
                a3=aa+ab
                c3=transform((-ll,0,0),0,a3,ab3,bb3)
                nu=(pb3[0]-c3[0],pb3[1]-c3[1],pb3[2]-c3[2])
                asp3=angle2vector(nz,nu)
                nl=(c3[0]-bb3[0],c3[1]-bb3[1],c3[2]-bb3[2])
                zl=cross(n,nl)
                asb3=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 4
        d2=bb4
        p1=bb4
        p2=pb4
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if ((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2)):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld)/(2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb)/(2*lc*ll),8))
                a4=aa+ab
                c4=transform((-ll,0,0),0,a4,ab4,bb4)
                nu=(pb4[0]-c4[0],pb4[1]-c4[1],pb4[2]-c4[2])
                asp4=angle2vector(nz,nu)
                nl=(c4[0]-bb4[0],c4[1]-bb4[1],c4[2]-bb4[2])
                zl=cross(n,nl)
                asb4=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 5
        d2=bb5
        p1=bb5
        p2=pb5
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if ((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2)):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld),8)/round((2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb),8)/round((2*lc*ll),8))
                a5=aa+ab
                c5=transform((-ll,0,0),0,a5,ab5,bb5)
                nu=(pb5[0]-c5[0],pb5[1]-c5[1],pb5[2]-c5[2])
                asp5=angle2vector(nz,nu)
                nl=(c5[0]-bb5[0],c5[1]-bb5[1],c5[2]-bb5[2])
                zl=cross(n,nl)
                asb5=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
        # Xác định góc quay của khớp chủ động trên chuỗi động thứ 6
        d2=bb6
        p1=bb6
        p2=pb6
        n=cross(d1,d2)
        k=(n[0]*p1[0]+n[1]*p1[1]+n[2]*p1[2]-n[0]*p2[0]-n[1]*p2[1]-n[2]*p2[2])/(n[0]*n[0]+n[1]*n[1]+n[2]*n[2])
        h=(p2[0]+n[0]*k,p2[1]+n[1]*k,p2[2]+n[2]*k)
        la=np.sqrt((h[0]-p2[0])*(h[0]-p2[0])+(h[1]-p2[1])*(h[1]-p2[1])+(h[2]-p2[2])*(h[2]-p2[2]))
        if ((lu*lu-la*la)>=0):
            lb=np.sqrt(lu*lu-la*la)
            lc=np.sqrt((h[0]-p1[0])*(h[0]-p1[0])+(h[1]-p1[1])*(h[1]-p1[1])+(h[2]-p1[2])*(h[2]-p1[2]))
            ld=np.sqrt(h[0]*h[0]+h[1]*h[1]+h[2]*h[2])
            if ((rb*lc)!=0) and ((lc*ll)!=0) and (round((rb*rb+lc*lc-ld*ld),8)<=round((2*rb*lc),8)) and (round((lc*lc+ll*ll-lb*lb),8)<=round((2*lc*ll),2)):
                aa=math.acos(round((rb*rb+lc*lc-ld*ld),8)/round((2*rb*lc),8))
                ab=math.acos(round((lc*lc+ll*ll-lb*lb),8)/round((2*lc*ll),8))
                a6=aa+ab
                c6=transform((-ll,0,0),0,a6,ab6,bb6)
                nu=(pb6[0]-c6[0],pb6[1]-c6[1],pb6[2]-c6[2])
                asp6=angle2vector(nz,nu)
                nl=(c6[0]-bb6[0],c6[1]-bb6[1],c6[2]-bb6[2])
                zl=cross(n,nl)
                asb6=angle2vector(nu,zl)
            else:
                check=0
        else:
            check=0

    if (check>0):
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

def clicked():
    global pp1,pp2,pp3,pp4,pp5,pp6,bb1,bb2,bb3,bb4,bb5,bb6,ab1,ab2,ab3,ab4,ab5,ab6
    pb0=[float(txt_position_x.get()),float(txt_position_y.get()),float(txt_position_z.get())]
    ax=float(txt_orientation_x.get())*np.pi/180
    ay=float(txt_orientation_y.get())*np.pi/180
    az=float(txt_orientation_z.get())*np.pi/180
    lsa=float(txt_angle.get())*np.pi/180
    # Tính tọa độ các điểm nối trên tấm dịch chuyển
    pp1=[rp*np.cos(0*np.pi/3),rp*np.sin(0*np.pi/3),0]
    pp2=[rp*np.cos(1*np.pi/3),rp*np.sin(1*np.pi/3),0]
    pp3=[rp*np.cos(2*np.pi/3),rp*np.sin(2*np.pi/3),0]
    pp4=[rp*np.cos(3*np.pi/3),rp*np.sin(3*np.pi/3),0]
    pp5=[rp*np.cos(4*np.pi/3),rp*np.sin(4*np.pi/3),0]
    pp6=[rp*np.cos(5*np.pi/3),rp*np.sin(5*np.pi/3),0]
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
    if (checkin(pb0,ax,ay,az)==1):
        lbl_result.configure(text="Vị trí và góc hướng này\nthuộc vùng làm việc")
    else:
        lbl_result.configure(text="Vị trí và góc hướng này\nkhông thuộc\nvùng làm việc")

# Các thông số của robot
lu=0.1
ll=0.05
lsa=30

# Các thông số của tấm dịch chuyển
rp=0.1

# Các thông số của bệ cố định
rb=0.1

# Vị trí tâm của tấm dịch chuyển theo hệ tọa độ gắn trên bệ cố định
pb0=[0,0,0.10]

# Các góc quay của tấm dịch chuyển
ax=0
ay=0
az=0

# Tạo giao diện chương trình
window=Tk()
window.geometry("1200x500")
window.title("Robot song song 6-RSS")
lbl_radius=Label(window,text="Bán kính:",fg="blue")
lbl_radius.place(x=20,y=20)
lbl_radius_platform=Label(window,text="Tấm")
lbl_radius_platform.place(x=30,y=40)
txt_radius_platform=Entry(window,width=14,justify=CENTER)
txt_radius_platform.insert(0,rp)
txt_radius_platform.place(x=60,y=41)
lbl_radius_base=Label(window,text="Bệ")
lbl_radius_base.place(x=30,y=60)
txt_radius_base=Entry(window,width=14,justify=CENTER)
txt_radius_base.insert(0,rb)
txt_radius_base.place(x=60,y=61)
lbl_length=Label(window,text="Chiều dài khâu:",fg="blue")
lbl_length.place(x=20,y=85)
lbl_length_up=Label(window,text="Trên")
lbl_length_up.place(x=30,y=105)
txt_length_up=Entry(window,width=14,justify=CENTER)
txt_length_up.insert(0,lu)
txt_length_up.place(x=60,y=106)
lbl_length_down=Label(window,text="Dưới")
lbl_length_down.place(x=30,y=125)
txt_length_down=Entry(window,width=14,justify=CENTER)
txt_length_down.insert(0,ll)
txt_length_down.place(x=60,y=126)
lbl_limit=Label(window,text="Giới hạn góc quay:",fg="blue")
lbl_limit.place(x=20,y=150)
lbl_angle=Label(window,text="Góc")
lbl_angle.place(x=30,y=170)
txt_angle=Entry(window,width=14,justify=CENTER)
txt_angle.insert(0,lsa)
txt_angle.place(x=60,y=171)
lbl_position=Label(window,text="Vị trí:",fg="blue")
lbl_position.place(x=20,y=195)
lbl_position_x=Label(window,text="x")
lbl_position_x.place(x=30,y=215)
txt_position_x=Entry(window,width=14,justify=CENTER)
txt_position_x.insert(0,pb0[0])
txt_position_x.place(x=60,y=216)
lbl_position_y=Label(window,text="y")
lbl_position_y.place(x=30,y=235)
txt_position_y=Entry(window,width=14,justify=CENTER)
txt_position_y.insert(0,pb0[1])
txt_position_y.place(x=60,y=236)
lbl_position_z=Label(window,text="z")
lbl_position_z.place(x=30,y=255)
txt_position_z=Entry(window,width=14,justify=CENTER)
txt_position_z.insert(0,pb0[2])
txt_position_z.place(x=60,y=256)
lbl_orientation=Label(window,text="Góc hướng:",fg="blue")
lbl_orientation.place(x=20,y=280)
lbl_orientation_x=Label(window,text="x")
lbl_orientation_x.place(x=30,y=300)
txt_orientation_x=Entry(window,width=14,justify=CENTER)
txt_orientation_x.insert(0,ax)
txt_orientation_x.place(x=60,y=301)
lbl_orientation_y=Label(window,text="y")
lbl_orientation_y.place(x=30,y=320)
txt_orientation_y=Entry(window,width=14,justify=CENTER)
txt_orientation_y.insert(0,ay)
txt_orientation_y.place(x=60,y=321)
lbl_orientation_z=Label(window,text="z")
lbl_orientation_z.place(x=30,y=340)
txt_orientation_z=Entry(window,width=14,justify=CENTER)
txt_orientation_z.insert(0,az)
txt_orientation_z.place(x=60,y=341)
btn_kinematic=Button(window, text="Giải động học ngược",command=clicked)
btn_kinematic.place(x=20,y=365,width=130)
lbl_result=Label(window,text="",fg="red")
lbl_result.place(x=20,y=395,width=130)
lbl_active_angle=Label(window,text="Góc quay chủ động:",fg="blue")
lbl_active_angle.place(x=1050,y=20)
lbl_active_angle_1=Label(window,text="1")
lbl_active_angle_1.place(x=1060,y=40)
txt_active_angle_1_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_1_value.place(x=1080,y=41)
lbl_active_angle_2=Label(window,text="2")
lbl_active_angle_2.place(x=1060,y=60)
txt_active_angle_2_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_2_value.place(x=1080,y=61)
lbl_active_angle_3=Label(window,text="3")
lbl_active_angle_3.place(x=1060,y=80)
txt_active_angle_3_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_3_value.place(x=1080,y=81)
lbl_active_angle_4=Label(window,text="4")
lbl_active_angle_4.place(x=1060,y=100)
txt_active_angle_4_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_4_value.place(x=1080,y=101)
lbl_active_angle_5=Label(window,text="5")
lbl_active_angle_5.place(x=1060,y=120)
txt_active_angle_5_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_5_value.place(x=1080,y=121)
lbl_active_angle_6=Label(window,text="6")
lbl_active_angle_6.place(x=1060,y=140)
txt_active_angle_6_value=Entry(window,width=15,justify=CENTER,state=DISABLED)
txt_active_angle_6_value.place(x=1080,y=141)
lbl_passive_angle=Label(window,text="Góc quay bị động trên:",fg="blue")
lbl_passive_angle.place(x=1050,y=165)
lbl_platform=Label(window,text="Tấm")
lbl_platform.place(x=1088,y=181)
lbl_base=Label(window,text="Bệ")
lbl_base.place(x=1138,y=181)
lbl_passive_angle_1=Label(window,text="1")
lbl_passive_angle_1.place(x=1060,y=199)
txt_passive_angle_1_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_1_platform_value.place(x=1080,y=200)
txt_passive_angle_1_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_1_base_value.place(x=1126,y=200)
lbl_passive_angle_2=Label(window,text="2")
lbl_passive_angle_2.place(x=1060,y=219)
txt_passive_angle_2_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_2_platform_value.place(x=1080,y=220)
txt_passive_angle_2_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_2_base_value.place(x=1126,y=220)
lbl_passive_angle_3=Label(window,text="3")
lbl_passive_angle_3.place(x=1060,y=239)
txt_passive_angle_3_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_3_platform_value.place(x=1080,y=240)
txt_passive_angle_3_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_3_base_value.place(x=1126,y=240)
lbl_passive_angle_4=Label(window,text="4")
lbl_passive_angle_4.place(x=1060,y=259)
txt_passive_angle_4_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_4_platform_value.place(x=1080,y=260)
txt_passive_angle_4_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_4_base_value.place(x=1126,y=260)
lbl_passive_angle_5=Label(window,text="5")
lbl_passive_angle_5.place(x=1060,y=279)
txt_passive_angle_5_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_5_platform_value.place(x=1080,y=280)
txt_passive_angle_5_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_5_base_value.place(x=1126,y=280)
lbl_passive_angle_6=Label(window,text="6")
lbl_passive_angle_6.place(x=1060,y=299)
txt_passive_angle_6_platform_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_6_platform_value.place(x=1080,y=300)
txt_passive_angle_6_base_value=Entry(window,width=7,justify=CENTER,state=DISABLED)
txt_passive_angle_6_base_value.place(x=1126,y=300)

window.mainloop()
