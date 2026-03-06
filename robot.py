
import browserbotics as bb
import math
import time

# =====================================================
#  COMPREHENSIVE SMART HOSPITAL ROBOTICS SYSTEM
#  
#  Features:
#  1. Multiple rooms: Surgery, Ward, Storage, Corridor
#  2. SURGI-BOT: Panda arm performing automated surgery
#  3. CARE-BOT: Pick & place + multi-room navigation
#  4. STERILE-BOT: UV sterilization robot with spiral patrol
#  5. All robots working simultaneously
# =====================================================

print("=" * 60)
print("  COMPREHENSIVE SMART HOSPITAL ROBOTICS SYSTEM")
print("=" * 60)
print("\nInitializing hospital environment...")

# ─────────────────────────────────────────────────────
#  HELPER FUNCTIONS FOR ENVIRONMENT
# ─────────────────────────────────────────────────────

def add_floor_tiles(x1, y1, x2, y2, c1='#ECEFF1', c2='#CFD8DC'):
    """Create checkered floor tiles"""
    step = 2.0
    x = x1
    tog = 0
    while x < x2:
        y = y1
        while y < y2:
            bb.createBody('box', halfExtent=[step/2, step/2, 0.01],
                          position=[x+step/2, y+step/2, 0.01],
                          color=c1 if tog%2==0 else c2, mass=0)
            y += step
            tog += 1
        x += step

def add_wall(x, y, hw, hd, hh, color='#F5F5F5'):
    """Create a wall section"""
    bb.createBody('box', halfExtent=[hw, hd, hh], 
                  position=[x, y, hh], color=color, mass=0)

def add_door_frame(dx, dy, color='#5D4037'):
    """Create door frame"""
    FH = 0.05
    DW = 0.55
    DH = 1.0
    bb.createBody('box', halfExtent=[FH, FH, DH], 
                  position=[dx-DW, dy, DH], color=color, mass=0)
    bb.createBody('box', halfExtent=[FH, FH, DH], 
                  position=[dx+DW, dy, DH], color=color, mass=0)
    bb.createBody('box', halfExtent=[DW+FH, FH, FH], 
                  position=[dx, dy, DH*2], color=color, mass=0)

def add_ceiling_light(cx, cy, h=2.4):
    """Create ceiling light fixture"""
    bb.createBody('box', halfExtent=[0.35, 0.35, 0.04], 
                  position=[cx, cy, h], color='#FAFAFA', mass=0)
    bb.createBody('sphere', radius=0.07, 
                  position=[cx, cy, h-0.05], color='#FFFDE7', mass=0)
    bb.createBody('box', halfExtent=[0.04, 0.04, 0.18], 
                  position=[cx, cy, h-0.18], color='#B0BEC5', mass=0)

def add_hospital_bed(bx, by, bz=0):
    """Create hospital bed with frame"""
    bb.createBody('box', halfExtent=[0.45, 1.0, 0.20], 
                  position=[bx, by, bz+0.20], color='#9E9E9E', mass=0)
    bb.createBody('box', halfExtent=[0.42, 0.90, 0.06], 
                  position=[bx, by, bz+0.46], color='white', mass=0)
    bb.createBody('box', halfExtent=[0.28, 0.15, 0.04], 
                  position=[bx, by+0.80, bz+0.54], color='#FFFDE7', mass=0)
    bb.createBody('box', halfExtent=[0.45, 0.04, 0.30], 
                  position=[bx, by+1.00, bz+0.50], color='#8B6914', mass=0)
    bb.createBody('box', halfExtent=[0.45, 0.04, 0.20], 
                  position=[bx, by-0.50, bz+0.40], color='#8B6914', mass=0)
    # Legs
    for lx, ly in [(-0.38, by-0.95), (0.38, by-0.95), 
                   (-0.38, by+0.95), (0.38, by+0.95)]:
        bb.createBody('box', halfExtent=[0.03, 0.03, 0.10],
                      position=[bx+lx, ly, bz+0.10], color='#757575', mass=0)

def add_patient(bx, by, bz=0, skin='#FDBCB4', gown='#E8B4B8'):
    """Create patient on bed"""
    ph = bz + 0.72
    bb.createBody('sphere', radius=0.12, 
                  position=[bx, by+0.82, ph+0.12], color=skin, mass=0)
    bb.createBody('box', halfExtent=[0.18, 0.35, 0.12], 
                  position=[bx, by+0.30, ph+0.00], color=gown, mass=0)
    bb.createBody('box', halfExtent=[0.05, 0.22, 0.06], 
                  position=[bx-0.25, by+0.35, ph+0.06], color=skin, mass=0)
    bb.createBody('box', halfExtent=[0.05, 0.22, 0.06], 
                  position=[bx+0.25, by+0.35, ph+0.06], color=skin, mass=0)
    bb.createBody('box', halfExtent=[0.09, 0.22, 0.08], 
                  position=[bx-0.12, by-0.25, ph-0.04], color=gown, mass=0)
    bb.createBody('box', halfExtent=[0.09, 0.22, 0.08], 
                  position=[bx+0.12, by-0.25, ph-0.04], color=gown, mass=0)

def add_iv_stand(sx, sy):
    """Create IV stand"""
    bb.createBody('box', halfExtent=[0.20, 0.20, 0.01], 
                  position=[sx, sy, 0.02], color='#9E9E9E', mass=0)
    bb.createBody('box', halfExtent=[0.015, 0.015, 0.85], 
                  position=[sx, sy, 0.85], color='#BDBDBD', mass=0)
    bb.createBody('box', halfExtent=[0.07, 0.025, 0.10], 
                  position=[sx, sy, 1.70], color='#80D8FF', mass=0)

def add_monitor(mx, my):
    """Create medical monitor"""
    bb.createBody('box', halfExtent=[0.22, 0.18, 0.32], 
                  position=[mx, my, 0.33], color='#795548', mass=0)
    bb.createBody('box', halfExtent=[0.20, 0.01, 0.14], 
                  position=[mx, my+0.02, 0.75], color='#111111', mass=0)
    bb.createBody('box', halfExtent=[0.17, 0.01, 0.11], 
                  position=[mx, my+0.01, 0.75], color='#00E676', mass=0)

def add_medicine_table(tx, ty):
    """Create medicine/supply table"""
    for lx, ly in [(-0.28, -0.18), (0.28, -0.18), 
                   (-0.28, 0.18), (0.28, 0.18)]:
        bb.createBody('box', halfExtent=[0.025, 0.025, 0.40],
                      position=[tx+lx, ty+ly, 0.40], color='#B0BEC5', mass=0)
    bb.createBody('box', halfExtent=[0.32, 0.22, 0.02],
                  position=[tx, ty, 0.82], color='#ECEFF1', mass=0)

def add_window(wx, wy, wz=1.30):
    """Create window"""
    bb.createBody('box', halfExtent=[0.60, 0.04, 0.45], 
                  position=[wx, wy, wz], color='#90CAF9', mass=0)
    bb.createBody('box', halfExtent=[0.65, 0.05, 0.50], 
                  position=[wx, wy+0.01, wz], color='#78909C', mass=0)

def add_plant(px, py):
    """Create decorative plant"""
    bb.createBody('box', halfExtent=[0.16, 0.16, 0.18], 
                  position=[px, py, 0.18], color='#546E7A', mass=0)
    bb.createBody('box', halfExtent=[0.022, 0.022, 0.32], 
                  position=[px, py, 0.70], color='#2E7D32', mass=0)
    for ox, oy, oz in [(-0.18, 0.08, 1.00), (0.18, 0.05, 1.05), 
                       (0.02, -0.14, 0.88)]:
        bb.createBody('box', halfExtent=[0.15, 0.22, 0.022],
                      position=[px+ox, py+oy, oz], color='#388E3C', mass=0)

def add_surgical_lamp(cx, cy):
    """Create large surgical overhead lamp"""
    bb.createBody('box', halfExtent=[0.45, 0.45, 0.05], 
                  position=[cx, cy, 2.40], color='#FAFAFA', mass=0)
    bb.createBody('box', halfExtent=[0.04, 0.04, 0.28], 
                  position=[cx, cy, 2.12], color='#90A4AE', mass=0)
    bb.createBody('box', halfExtent=[0.38, 0.38, 0.03], 
                  position=[cx, cy, 2.38], color='#FFFDE7', mass=0)
    for lx in [-0.20, 0.0, 0.20]:
        for ly in [-0.14, 0.14]:
            bb.createBody('sphere', radius=0.032,
                          position=[cx+lx, cy+ly, 2.35], 
                          color='#FFF9C4', mass=0)

def add_instrument_table(tx, ty):
    """Create surgical instrument table"""
    for lx, ly in [(-0.28, -0.18), (0.28, -0.18), 
                   (-0.28, 0.18), (0.28, 0.18)]:
        bb.createBody('box', halfExtent=[0.025, 0.025, 0.42],
                      position=[tx+lx, ty+ly, 0.42], color='#CFD8DC', mass=0)
    bb.createBody('box', halfExtent=[0.30, 0.20, 0.015],
                  position=[tx, ty, 0.85], color='#ECEFF1', mass=0)
    # Instruments
    bb.createBody('box', halfExtent=[0.10, 0.008, 0.006], 
                  position=[tx-0.12, ty-0.08, 0.872], color='#B0BEC5', mass=0)
    bb.createBody('box', halfExtent=[0.09, 0.005, 0.005], 
                  position=[tx-0.10, ty+0.02, 0.872], color='#CFD8DC', mass=0)
    bb.createBody('box', halfExtent=[0.08, 0.007, 0.006], 
                  position=[tx+0.08, ty-0.06, 0.872], color='#90A4AE', mass=0)
    bb.createBody('sphere', radius=0.025, 
                  position=[tx+0.20, ty+0.10, 0.875], color='#B3E5FC', mass=0)

def add_operating_table(ox, oy):
    """Create operating table"""
    # Legs
    bb.createBody('box', halfExtent=[0.06, 0.06, 0.40], 
                  position=[ox-0.35, oy, 0.40], color='#546E7A', mass=0)
    bb.createBody('box', halfExtent=[0.06, 0.06, 0.40], 
                  position=[ox+0.35, oy, 0.40], color='#546E7A', mass=0)
    bb.createBody('box', halfExtent=[0.06, 0.06, 0.40], 
                  position=[ox-0.35, oy+0.90, 0.40], color='#546E7A', mass=0)
    bb.createBody('box', halfExtent=[0.06, 0.06, 0.40], 
                  position=[ox+0.35, oy+0.90, 0.40], color='#546E7A', mass=0)
    # Table top
    bb.createBody('box', halfExtent=[0.45, 1.10, 0.04], 
                  position=[ox, oy+0.45, 0.82], color='#B0BEC5', mass=0)
    # Mattress
    bb.createBody('box', halfExtent=[0.42, 1.05, 0.04], 
                  position=[ox, oy+0.45, 0.88], color='#E0E0E0', mass=0)
    # Pillow
    bb.createBody('box', halfExtent=[0.28, 0.14, 0.04], 
                  position=[ox, oy+1.30, 0.96], color='#FFFFFF', mass=0)

def add_surgery_patient(ox, oy):
    """Create patient on operating table"""
    pz = 0.94
    bb.createBody('box', halfExtent=[0.18, 0.38, 0.10], 
                  position=[ox, oy+0.45, pz+0.10], color='#B3E5FC', mass=0)
    bb.createBody('sphere', radius=0.13, 
                  position=[ox, oy+1.28, pz+0.22], color='#FDBCB4', mass=0)
    bb.createBody('box', halfExtent=[0.05, 0.30, 0.06], 
                  position=[ox-0.26, oy+0.55, pz+0.06], color='#FDBCB4', mass=0)
    bb.createBody('box', halfExtent=[0.05, 0.30, 0.06], 
                  position=[ox+0.26, oy+0.55, pz+0.06], color='#FDBCB4', mass=0)
    bb.createBody('box', halfExtent=[0.08, 0.30, 0.08], 
                  position=[ox-0.10, oy-0.35, pz+0.06], color='#B3E5FC', mass=0)
    bb.createBody('box', halfExtent=[0.08, 0.30, 0.08], 
                  position=[ox+0.10, oy-0.35, pz+0.06], color='#B3E5FC', mass=0)
    # Surgical drape
    bb.createBody('box', halfExtent=[0.44, 0.60, 0.012], 
                  position=[ox, oy+0.20, pz+0.22], color='#388E3C', mass=0)

# ─────────────────────────────────────────────────────
#  BUILD WARD ROOM (ROOM 1)
# ─────────────────────────────────────────────────────

def build_ward():
    """Build patient ward with 3 beds"""
    print("Building Ward Room...")
    bb.addGroundPlane()
    add_floor_tiles(-8, -8, 8, 8, '#ECEFF1', '#CFD8DC')
    
    WH = 1.2
    WT = 0.06
    
    # Walls
    add_wall(-8, 0, WT, 8, WH, '#F5F5F5')
    add_wall(8, 0, WT, 8, WH, '#F5F5F5')
    add_wall(0, 8, 8, WT, WH, '#F5F5F5')
    add_wall(-4.6, -8, 3.4, WT, WH, '#F5F5F5')
    add_wall(4.6, -8, 3.4, WT, WH, '#F5F5F5')
    bb.createBody('box', halfExtent=[1.1, WT, 0.22],
                  position=[0, -8, 1.22], color='#F5F5F5', mass=0)
    add_door_frame(0, -8)
    
    # Lighting
    for cx, cy in [(0, 0), (-4, 4), (4, 4), (-4, -2), (4, -2)]:
        add_ceiling_light(cx, cy)
    
    # Windows
    add_window(2, 7.95)
    add_window(-2, 7.95)
    
    # Hospital beds with patients
    beds = [(0.0, 2.0), (-4.0, 2.0), (-4.0, 6.0)]
    gowns = ['#E8B4B8', '#B2EBF2', '#C8E6C9']
    
    for i, (bx, by) in enumerate(beds):
        add_hospital_bed(bx, by)
        add_patient(bx, by, gown=gowns[i])
        add_iv_stand(bx+0.85, by+0.90)
        add_monitor(bx-1.10, by+0.50)
    
    # Nursing station
    bb.createBody('box', halfExtent=[0.80, 0.30, 0.50], 
                  position=[5.5, 0.5, 0.50], color='#ECEFF1', mass=0)
    bb.createBody('box', halfExtent=[0.85, 0.32, 0.02], 
                  position=[5.5, 0.5, 1.02], color='#CFD8DC', mass=0)
    
    # Supply cabinet
    bb.createBody('box', halfExtent=[0.40, 0.15, 0.55], 
                  position=[-7.2, 4.0, 0.80], color='white', mass=0)
    bb.createBody('box', halfExtent=[0.40, 0.15, 0.02], 
                  position=[-7.2, 4.0, 1.38], color='#DDDDDD', mass=0)
    
    # Plants
    add_plant(6.5, -5.0)
    add_plant(-6.5, -5.0)
    
    # Medicine table with objects
    add_medicine_table(4.0, 5.0)
    med_obj = bb.createBody('box', halfExtent=[0.09, 0.09, 0.09],
                            position=[4.0, 5.0, 0.93], 
                            color='#FF5722', mass=0.1)
    supply_obj = bb.createBody('box', halfExtent=[0.09, 0.09, 0.09],
                               position=[4.0, 4.7, 0.93], 
                               color='#1565C0', mass=0.1)
    
    print("  ✓ Ward Room complete (3 beds, medicine table)")
    return med_obj, supply_obj

# ─────────────────────────────────────────────────────
#  BUILD SURGERY ROOM (ROOM 2)
# ─────────────────────────────────────────────────────

def build_surgery_room():
    """Build operating theatre with surgical robot"""
    print("Building Surgery Room...")
    OX = -16.0
    OY = 0.0
    
    add_floor_tiles(OX-5, OY-5, OX+5, OY+5, '#E3F2FD', '#BBDEFB')
    
    WH = 1.2
    WT = 0.06
    
    # Walls
    add_wall(OX-5, OY, WT, 5, WH, '#E8EAF6')
    add_wall(OX+5, OY, WT, 5, WH, '#E8EAF6')
    add_wall(OX, OY+5, 5, WT, WH, '#E8EAF6')
    add_wall(OX-3.4, OY-5, 1.6, WT, WH, '#E8EAF6')
    add_wall(OX+3.4, OY-5, 1.6, WT, WH, '#E8EAF6')
    bb.createBody('box', halfExtent=[1.1, WT, 0.22],
                  position=[OX, OY-5, 1.22], color='#E8EAF6', mass=0)
    add_door_frame(OX, OY-5)
    
    # Surgical lamp
    add_surgical_lamp(OX, OY+0.45)
    
    # Windows
    add_window(OX+2, OY+4.95)
    add_window(OX-2, OY+4.95)
    
    # UV sterilization lamp on wall
    bb.createBody('box', halfExtent=[0.08, 0.04, 0.24], 
                  position=[OX-4.9, OY+2.5, 1.10], color='#6A1B9A', mass=0)
    bb.createBody('sphere', radius=0.07, 
                  position=[OX-4.9, OY+2.5, 1.38], color='#CE93D8', mass=0)
    
    # Emergency line
    bb.createBody('box', halfExtent=[4.8, 0.06, 0.012], 
                  position=[OX, OY-4.5, 0.012], color='#F44336', mass=0)
    
    # Operating table and patient
    add_operating_table(OX, OY-0.45)
    add_surgery_patient(OX, OY-0.45)
    
    # Instrument table
    add_instrument_table(OX+1.8, OY+0.8)
    
    # Medical equipment
    add_monitor(OX-1.80, OY-0.50)
    add_iv_stand(OX+0.90, OY-1.20)
    
    # Anesthesia machine
    bb.createBody('box', halfExtent=[0.28, 0.20, 0.55], 
                  position=[OX-1.8, OY+1.8, 0.55], color='#ECEFF1', mass=0)
    bb.createBody('box', halfExtent=[0.25, 0.18, 0.02], 
                  position=[OX-1.8, OY+1.8, 1.12], color='#CFD8DC', mass=0)
    bb.createBody('sphere', radius=0.05, 
                  position=[OX-1.6, OY+1.8, 0.90], color='#29B6F6', mass=0)
    bb.createBody('sphere', radius=0.05, 
                  position=[OX-2.0, OY+1.8, 0.90], color='#EF9A9A', mass=0)
    
    # Surgeon assistant
    bb.createBody('box', halfExtent=[0.14, 0.12, 0.40], 
                  position=[OX+1.2, OY-0.20, 0.70], color='#E8EAF6', mass=0)
    bb.createBody('sphere', radius=0.12, 
                  position=[OX+1.2, OY-0.20, 1.22], color='#FDBCB4', mass=0)
    bb.createBody('sphere', radius=0.13, 
                  position=[OX+1.2, OY-0.20, 1.34], color='#B0BEC5', mass=0)
    bb.createBody('box', halfExtent=[0.08, 0.02, 0.05], 
                  position=[OX+1.2, OY-0.09, 1.16], color='#B0BEC5', mass=0)
    
    # Panda arm base
    bb.createBody('box', halfExtent=[0.30, 0.30, 0.06], 
                  position=[OX-1.2, OY+0.45, 0.06], color='#37474F', mass=0)
    bb.createBody('box', halfExtent=[0.28, 0.28, 0.28], 
                  position=[OX-1.2, OY+0.45, 0.34], color='#455A64', mass=0)
    for wx, wy in [(-0.22, -0.22), (0.22, -0.22), 
                   (-0.22, 0.22), (0.22, 0.22)]:
        bb.createBody('sphere', radius=0.07,
                      position=[OX-1.2+wx, OY+0.45+wy, 0.07], 
                      color='#212121', mass=0)
    
    # Load Panda arm
    surg_arm = bb.loadURDF('panda.urdf', [OX-1.2, OY+0.45, 0.62], fixedBase=True)
    
    print("  ✓ Surgery Room complete (Panda arm, operating table)")
    return surg_arm, OX, OY

# ─────────────────────────────────────────────────────
#  BUILD CORRIDOR
# ─────────────────────────────────────────────────────

def build_corridor():
    """Build connecting corridor between rooms"""
    print("Building Corridor...")
    add_floor_tiles(-16, -12, 0, -8, '#EEEEEE', '#E0E0E0')
    bb.createBody('box', halfExtent=[0.06, 2.0, 1.2], 
                  position=[-8, -10, 1.2], color='#F5F5F5', mass=0)
    bb.createBody('box', halfExtent=[0.06, 2.0, 1.2], 
                  position=[-16, -10, 1.2], color='#E8EAF6', mass=0)
    
    # Direction arrows
    for ax in [-4, -8, -12]:
        bb.createBody('box', halfExtent=[0.40, 0.06, 0.012],
                      position=[ax, -10, 0.012], color='#90CAF9', mass=0)
    
    print("  ✓ Corridor complete")

# ─────────────────────────────────────────────────────
#  CARE-BOT (MOBILE ROBOT WITH PICK & PLACE)
# ─────────────────────────────────────────────────────

def _make_robot_parts(cx, cy, has_box=False, box_color='#FF5722', arm_down=False):
    """Create robot body parts"""
    parts = []
    z = 0.10
    arm_z = z+0.08 if arm_down else z+0.22
    
    # Wheels
    for wx, wy in [(-0.20, -0.22), (0.20, -0.22), 
                   (-0.20, 0.22), (0.20, 0.22)]:
        parts.append(bb.createBody('sphere', radius=0.06,
                                   position=[cx+wx, cy+wy, 0.06], 
                                   color='#212121', mass=0))
    
    # Base
    parts.append(bb.createBody('box', halfExtent=[0.24, 0.24, 0.06],
                               position=[cx, cy, z], color='#0277BD', mass=0))
    
    # Body
    parts.append(bb.createBody('box', halfExtent=[0.20, 0.20, 0.15],
                               position=[cx, cy, z+0.21], color='#01579B', mass=0))
    
    # Head
    parts.append(bb.createBody('sphere', radius=0.13,
                               position=[cx, cy, z+0.50], color='#E1F5FE', mass=0))
    
    # Eyes
    parts.append(bb.createBody('sphere', radius=0.035,
                               position=[cx-0.07, cy+0.11, z+0.54], 
                               color='#00E5FF', mass=0))
    parts.append(bb.createBody('sphere', radius=0.035,
                               position=[cx+0.07, cy+0.11, z+0.54], 
                               color='#00E5FF', mass=0))
    
    # Left arm (sensor)
    parts.append(bb.createBody('box', halfExtent=[0.04, 0.04, 0.14],
                               position=[cx-0.26, cy, z+0.22], 
                               color='#0288D1', mass=0))
    parts.append(bb.createBody('sphere', radius=0.045,
                               position=[cx-0.26, cy, z+0.06], 
                               color='#90CAF9', mass=0))
    
    # Right arm (gripper)
    parts.append(bb.createBody('box', halfExtent=[0.04, 0.04, 0.14],
                               position=[cx+0.26, cy, arm_z], 
                               color='#0288D1', mass=0))
    parts.append(bb.createBody('sphere', radius=0.045,
                               position=[cx+0.26, cy, arm_z-0.14], 
                               color='#EF5350', mass=0))
    
    # Carried box
    if has_box:
        parts.append(bb.createBody('box', halfExtent=[0.09, 0.09, 0.09],
                                   position=[cx+0.26, cy, arm_z-0.26],
                                   color=box_color, mass=0))
    
    return parts

def _clear(parts):
    """Remove robot parts"""
    for b in parts:
        bb.removeBody(b)

def navigate_robot(parts, x0, y0, x1, y1, steps=50, 
                   has_box=False, box_color='#FF5722'):
    """Move robot from point A to point B"""
    for s in range(steps+1):
        t = s / float(steps)
        cx = x0 + (x1-x0) * t
        cy = y0 + (y1-y0) * t
        _clear(parts)
        parts[:] = _make_robot_parts(cx, cy, has_box=has_box, box_color=box_color)
        time.sleep(0.035)
    return cx, cy

def pick_anim(parts, cx, cy, has_box, box_color):
    """Picking animation (arm down/up)"""
    for s in range(18):
        _clear(parts)
        parts[:] = _make_robot_parts(cx, cy, has_box=has_box,
                                     box_color=box_color, arm_down=(s>8))
        time.sleep(0.03)

# ─────────────────────────────────────────────────────
#  STERILE-BOT (UV STERILIZATION ROBOT)
# ─────────────────────────────────────────────────────

_sterile_parts = []

def spawn_sterile(cx, cy):
    """Create/update sterilization robot"""
    global _sterile_parts
    _clear(_sterile_parts)
    _sterile_parts = []
    
    vz = 0.05
    
    # Base
    _sterile_parts.append(bb.createBody('box', halfExtent=[0.24, 0.24, 0.045],
                                        position=[cx, cy, vz], 
                                        color='#1A237E', mass=0))
    
    # UV dome
    _sterile_parts.append(bb.createBody('sphere', radius=0.20,
                                        position=[cx, cy, vz+0.04], 
                                        color='#283593', mass=0))
    
    # UV emitter
    _sterile_parts.append(bb.createBody('sphere', radius=0.05,
                                        position=[cx, cy+0.10, vz+0.22], 
                                        color='#7C4DFF', mass=0))
    
    # UV light bars
    _sterile_parts.append(bb.createBody('box', halfExtent=[0.13, 0.013, 0.009],
                                        position=[cx-0.20, cy, vz], 
                                        color='#FF6F00', mass=0))
    _sterile_parts.append(bb.createBody('box', halfExtent=[0.13, 0.013, 0.009],
                                        position=[cx+0.20, cy, vz], 
                                        color='#FF6F00', mass=0))
    
    # Top sensor
    _sterile_parts.append(bb.createBody('sphere', radius=0.09,
                                        position=[cx, cy, vz+0.30], 
                                        color='#E040FB', mass=0))

# ═════════════════════════════════════════════════════
#  BUILD COMPLETE HOSPITAL
# ═════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("  BUILDING COMPLETE HOSPITAL SYSTEM")
print("=" * 60)

med_obj, supply_obj = build_ward()
surg_arm, SRX, SRY = build_surgery_room()
build_corridor()

print("\n" + "=" * 60)
print("  HOSPITAL CONSTRUCTION COMPLETE")
print("=" * 60)

# ─── CONFIGURE SURGI-BOT (Panda Arm) ────────────────
print("\nConfiguring SURGI-BOT joints...")
surg_joints = []
for i in range(bb.getNumJoints(surg_arm)):
    jname, jtype, jlimits = bb.getJointInfo(surg_arm, i)
    if jtype != 'fixed':
        surg_joints.append((i, jname, jlimits))
        bb.addDebugSlider('J_'+jname, sum(jlimits)/2.0, *jlimits)

print(f"  ✓ {len(surg_joints)} joints configured")

# ─── CONTROL SLIDERS ─────────────────────────────────
bb.addDebugSlider('START_MISSION', 0.0, 0.0, 1.0)
bb.addDebugSlider('STERILE_SPEED', 1.0, 0.2, 4.0)
bb.addDebugSlider('AUTO_SURGERY', 1.0, 0.0, 1.0)

# ═════════════════════════════════════════════════════
#  SURGI-BOT SURGICAL WAYPOINTS
# ═════════════════════════════════════════════════════

print("\nProgramming surgical procedure...")
surg_waypoints = []
if len(surg_joints) >= 7:
    surg_waypoints.append([
        (surg_joints[0][0], 0.00), (surg_joints[1][0], -0.50),
        (surg_joints[2][0], 0.00), (surg_joints[3][0], -1.80),
        (surg_joints[4][0], 0.00), (surg_joints[5][0], 1.40),
        (surg_joints[6][0], 0.00),
    ])
    surg_waypoints.append([
        (surg_joints[0][0], 0.30), (surg_joints[1][0], -0.20),
        (surg_joints[2][0], 0.10), (surg_joints[3][0], -2.10),
        (surg_joints[4][0], -0.10), (surg_joints[5][0], 2.00),
        (surg_joints[6][0], 0.40),
    ])
    surg_waypoints.append([
        (surg_joints[0][0], 0.30), (surg_joints[1][0], 0.10),
        (surg_joints[2][0], 0.10), (surg_joints[3][0], -2.30),
        (surg_joints[4][0], -0.10), (surg_joints[5][0], 2.40),
        (surg_joints[6][0], 0.40),
    ])
    surg_waypoints.append([
        (surg_joints[0][0], -0.30), (surg_joints[1][0], 0.10),
        (surg_joints[2][0], -0.10), (surg_joints[3][0], -2.30),
        (surg_joints[4][0], 0.10), (surg_joints[5][0], 2.40),
        (surg_joints[6][0], -0.40),
    ])
    surg_waypoints.append([
        (surg_joints[0][0], -0.30), (surg_joints[1][0], -0.50),
        (surg_joints[2][0], -0.10), (surg_joints[3][0], -1.80),
        (surg_joints[4][0], 0.10), (surg_joints[5][0], 1.40),
        (surg_joints[6][0], -0.40),
    ])

print(f"  ✓ {len(surg_waypoints)} surgical phases programmed")

surg_wp_idx = 0
surg_wp_timer = 0.0
surg_wp_period = 2.5

surg_current = {}
surg_target = {}
for i, jname, jlimits in surg_joints:
    surg_current[i] = sum(jlimits)/2.0
    surg_target[i] = sum(jlimits)/2.0

# ═════════════════════════════════════════════════════
#  CARE-BOT MISSION WAYPOINTS
# ═════════════════════════════════════════════════════

CARE_START = [4.0, 3.5]
care_parts = _make_robot_parts(*CARE_START)
robot_pos = list(CARE_START)
mission_phase = 0
mission_active = False
carry_color = '#FF5722'

TABLE_POS = [4.0, 5.0]
BED_A = [0.0, 2.0]
TABLE2_POS = [4.0, 4.7]
WARD_EXIT = [0.0, -8.0]
CORR_MID = [-8.0, -10.0]
SURG_ENTER = [SRX, SRY-5.0]
SURG_TABLE = [SRX+1.8, SRY+0.8]

# ═════════════════════════════════════════════════════
#  STERILE-BOT STATE
# ═════════════════════════════════════════════════════

s_angle = 0.0
s_radius = 1.5
s_dir = 1
S_MAX = 6.5
S_MIN = 0.5
spawn_sterile(0.0, 0.0)

# ═════════════════════════════════════════════════════
#  SIMULATION STATUS
# ═════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("  SMART HOSPITAL SYSTEM - OPERATIONAL")
print("=" * 60)
print("\n🏥 HOSPITAL LAYOUT:")
print("  • Ward Room (0,0): 3 patient beds, medicine table")
print("  • Surgery Room (-16,0): Operating theatre, Panda arm")
print("  • Corridor: Connecting passage")
print("\n🤖 ACTIVE ROBOTS:")
print("  • SURGI-BOT: Performing automated surgery")
print("  • CARE-BOT: Pick & place, multi-room navigation")
print("  • STERILE-BOT: UV sterilization patrol")
print("\n🎮 CONTROLS:")
print("  • AUTO_SURGERY=1: Surgical robot operates")
print("  • START_MISSION=1: Care robot begins mission")
print("  • STERILE_SPEED: UV patrol speed (0.2-4.0)")
print("\n📋 CARE-BOT MISSION:")
print("  1. Navigate to medicine table")
print("  2. Pick medicine box")
print("  3. Deliver to patient bed")
print("  4. Return to pick surgical supply")
print("  5. Navigate through corridor")
print("  6. Enter surgery room")
print("  7. Place supply on instrument table")
print("  8. Return to ward")
print("\nPress Ctrl+C to stop\n")
print("=" * 60)

# ═════════════════════════════════════════════════════
#  MAIN SIMULATION LOOP
# ═════════════════════════════════════════════════════

while True:
    dt = 0.05
    
    # ── SURGI-BOT: Automated surgical motion ─────────
    auto_surg = bb.readDebugParameter('AUTO_SURGERY')
    if auto_surg > 0.5 and len(surg_waypoints) > 0:
        surg_wp_timer += dt
        if surg_wp_timer >= surg_wp_period:
            surg_wp_timer = 0.0
            surg_wp_idx = (surg_wp_idx + 1) % len(surg_waypoints)
            for jidx, jtarget in surg_waypoints[surg_wp_idx]:
                surg_target[jidx] = jtarget
        
        alpha = min(1.0, dt * 3.0)
        for i, jname, jlimits in surg_joints:
            surg_current[i] += (surg_target[i] - surg_current[i]) * alpha
            bb.setJointMotorControl(surg_arm, i, targetPosition=surg_current[i])
    else:
        for i, jname, jlimits in surg_joints:
            jp = bb.readDebugParameter('J_'+jname)
            bb.setJointMotorControl(surg_arm, i, targetPosition=jp)
    
    # ── STERILE-BOT: Spiral UV patrol ───────────────
    spd = bb.readDebugParameter('STERILE_SPEED')
    s_angle += 0.05 * spd
    s_radius += 0.010 * spd * s_dir
    if s_radius >= S_MAX:
        s_dir = -1
    elif s_radius <= S_MIN:
        s_dir = 1
    sx = max(-7.0, min(7.0, s_radius * math.cos(s_angle)))
    sy = max(-7.0, min(7.0, s_radius * math.sin(s_angle)))
    spawn_sterile(sx, sy)
    
    # ── CARE-BOT: Mission execution ──────────────────
    trigger = bb.readDebugParameter('START_MISSION')
    if trigger > 0.5 and not mission_active:
        mission_active = True
        mission_phase = 1
        print("\n>>> CARE-BOT MISSION ACTIVATED <<<")
    
    if mission_phase == 1:
        print("[Phase 1/8] Navigating to medicine table...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                TABLE_POS[0], TABLE_POS[1], steps=45)
        robot_pos = [cx, cy]
        mission_phase = 2
    
    elif mission_phase == 2:
        print("[Phase 2/8] Picking medicine box...")
        pick_anim(care_parts, robot_pos[0], robot_pos[1], False, '#FF5722')
        bb.removeBody(med_obj)
        carry_color = '#FF5722'
        _clear(care_parts)
        care_parts[:] = _make_robot_parts(*robot_pos, has_box=True, box_color=carry_color)
        pick_anim(care_parts, robot_pos[0], robot_pos[1], True, carry_color)
        print("  ✓ Medicine picked!")
        mission_phase = 3
    
    elif mission_phase == 3:
        print("[Phase 3/8] Delivering medicine to patient bed...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                BED_A[0]+0.8, BED_A[1], steps=50,
                                has_box=True, box_color=carry_color)
        robot_pos = [cx, cy]
        pick_anim(care_parts, robot_pos[0], robot_pos[1], True, carry_color)
        bb.createBody('box', halfExtent=[0.09, 0.09, 0.09],
                      position=[BED_A[0]+0.5, BED_A[1]+0.3, 1.10],
                      color=carry_color, mass=0)
        _clear(care_parts)
        care_parts[:] = _make_robot_parts(*robot_pos, has_box=False)
        pick_anim(care_parts, robot_pos[0], robot_pos[1], False, carry_color)
        print("  ✓ Medicine delivered to patient!")
        mission_phase = 4
    
    elif mission_phase == 4:
        print("[Phase 4/8] Picking surgical supply...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                TABLE2_POS[0], TABLE2_POS[1], steps=40)
        robot_pos = [cx, cy]
        pick_anim(care_parts, robot_pos[0], robot_pos[1], False, '#1565C0')
        bb.removeBody(supply_obj)
        carry_color = '#1565C0'
        _clear(care_parts)
        care_parts[:] = _make_robot_parts(*robot_pos, has_box=True, box_color=carry_color)
        pick_anim(care_parts, robot_pos[0], robot_pos[1], True, carry_color)
        print("  ✓ Surgical supply picked!")
        mission_phase = 5
    
    elif mission_phase == 5:
        print("[Phase 5/8] Navigating to corridor...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                WARD_EXIT[0], WARD_EXIT[1], steps=55,
                                has_box=True, box_color=carry_color)
        robot_pos = [cx, cy]
        mission_phase = 6
    
    elif mission_phase == 6:
        print("[Phase 6/8] Crossing corridor to surgery room...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                CORR_MID[0], CORR_MID[1], steps=40,
                                has_box=True, box_color=carry_color)
        robot_pos = [cx, cy]
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                SURG_ENTER[0], SURG_ENTER[1], steps=40,
                                has_box=True, box_color=carry_color)
        robot_pos = [cx, cy]
        mission_phase = 7
    
    elif mission_phase == 7:
        print("[Phase 7/8] Delivering supply to surgery room...")
        cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                SURG_TABLE[0]-0.8, SURG_TABLE[1], steps=50,
                                has_box=True, box_color=carry_color)
        robot_pos = [cx, cy]
        pick_anim(care_parts, robot_pos[0], robot_pos[1], True, carry_color)
        bb.createBody('box', halfExtent=[0.09, 0.09, 0.09],
                      position=[SURG_TABLE[0], SURG_TABLE[1], 0.93],
                      color=carry_color, mass=0)
        _clear(care_parts)
        care_parts[:] = _make_robot_parts(*robot_pos, has_box=False)
        pick_anim(care_parts, robot_pos[0], robot_pos[1], False, carry_color)
        print("  ✓ Supply delivered to OR!")
        mission_phase = 8
    
    elif mission_phase == 8:
        print("[Phase 8/8] Returning to ward base...")
        for wp in [SURG_ENTER, CORR_MID, WARD_EXIT, CARE_START]:
            cx, cy = navigate_robot(care_parts, robot_pos[0], robot_pos[1],
                                    wp[0], wp[1], steps=45)
            robot_pos = [cx, cy]
        
        print("\n" + "=" * 60)
        print("  ✅ ALL MISSIONS COMPLETE!")
        print("=" * 60)
        print("  • SURGI-BOT: Performing surgery (automatic)")
        print("  • STERILE-BOT: UV patrol continues")
        print("  • CARE-BOT: Mission accomplished, standing by")
        print("=" * 60)
        mission_active = False
        mission_phase = 0
    
    time.sleep(dt)
