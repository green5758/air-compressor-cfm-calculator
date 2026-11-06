import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "AirSpecPro"
SITE_TAGLINE = "Air Compressor SCFM @ 90 PSI, Tank Gallon, HVLP / Sandblaster & Piping Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/airspecpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "airspecpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Ingersoll Rand SS5L5 / Type-30 5 HP 60-Gallon & 80-Gallon 230V Single/Two-Stage Air Compressor",
        "category": "60–80 Gal Stationary Compressor",
        "rating": "4.8 ★ (3,850+ reviews)",
        "badge": "#1 Garage Shop Compressor",
        "specs": "18.1 SCFM @ 90 PSI | 100% Cast-Iron Pump (15,000+ Hr Life) | 135–175 PSI Max | ASME 60/80 Gal Tank",
        "keyword": "Ingersoll+Rand+SS5L5+5+HP+60+Gallon+80+Gallon+Air+Compressor"
    },
    {
        "title": "California Air Tools 10020C / 20020D 2.0 HP 10-Gal & 20-Gal Ultra-Quiet (70 dBA) Oil-Free Compressor",
        "category": "Ultra-Quiet Shop Compressor",
        "rating": "4.8 ★ (6,400+ reviews)",
        "badge": "#1 Ultra-Quiet 70 dBA Unit",
        "specs": "6.40 SCFM @ 40 PSI / 5.30 SCFM @ 90 PSI | Only 70 dBA Noise | Dual-Piston Oil-Free Pump (3,000+ Hrs)",
        "keyword": "California+Air+Tools+10020C+2.0+HP+10+Gallon+20+Gallon+Ultra+Quiet+Air+Compressor"
    },
    {
        "title": "RapidAir Maxline M7500 3/4-Inch × 100-Foot Master Compressed Air Garage Piping System Kit",
        "category": "3/4\" Shop Air Piping Kit",
        "rating": "4.8 ★ (4,900+ reviews)",
        "badge": "#1 Garage Air Piping Kit",
        "specs": "100-Ft Aluminum-Core HDPE Tubing (175 PSI) | 3× Wall Manifold Outlets w/ Drains | Zero Rust or Glue",
        "keyword": "RapidAir+Maxline+M7500+3+4+Inch+100+Ft+Compressed+Air+Piping+Kit"
    },
    {
        "title": "Ingersoll Rand 2235TiMAX 1/2-Inch Drive Titanium Duty Air Impact Wrench (1,350 Ft-Lb Nut-Busting)",
        "category": "Titanium Pneumatic Impact Gun",
        "rating": "4.9 ★ (11,200+ reviews)",
        "badge": "#1 Mechanic's Air Impact",
        "specs": "1,350 Ft-Lb Breakaway Torque | Weighs Only 4.6 Lbs | Titanium Hammer Case | Twin-Hammer Mechanism",
        "keyword": "Ingersoll+Rand+2235TiMAX+1+2+Inch+Titanium+Air+Impact+Wrench"
    },
    {
        "title": "3M Performance Industrial HVLP Spray Gun Starter Kit w/ PPS 2.0 Quick-Change Atomizing Heads",
        "category": "HVLP Automotive Paint Gun",
        "rating": "4.9 ★ (3,100+ reviews)",
        "badge": "#1 Auto Body HVLP System",
        "specs": "13.0 SCFM @ 29 PSI | Includes 1.2, 1.3, 1.4, 1.8 & 2.0mm Nozzles | Composite Body + 3M PPS 2.0 Cups",
        "keyword": "3M+Performance+Spray+Gun+Kit+HVLP+PPS+2.0"
    },
    {
        "title": "NANPU / DeVilbiss 1/2\" NPT 3-Stage Compressed Air Drying System (Regulator + Coalescing + Desiccant)",
        "category": "3-Stage Paint & Plasma Air Dryer",
        "rating": "4.8 ★ (4,500+ reviews)",
        "badge": "#1 Cure for Water in Paint/Plasma",
        "specs": "5-Micron Water Trap + 0.01-Micron Oil Coalescer + Color-Changing Desiccant Beads (-40°F Dew Point)",
        "keyword": "3+Stage+Compressed+Air+Dryer+Desiccant+Filter+Regulator+1+2+NPT"
    },
    {
        "title": "BluBird / Goodyear 3/8-Inch × 50-Foot 100% Rubber Heavy-Duty Retractable Air Hose Reel (300 PSI)",
        "category": "Retractable Air Hose Reel",
        "rating": "4.9 ★ (8,700+ reviews)",
        "badge": "#1 Cold-Weather Rubber Reel",
        "specs": "100% EPDM Rubber Hose (Stays Flat to -50°F) | Dual-Arm Steel Frame | 12-Point Ratchet Lock",
        "keyword": "BluBird+Goodyear+3+8+Inch+50+Foot+Retractable+Air+Hose+Reel"
    },
    {
        "title": "DEWALT DXCM601 / DXCM801 60-Gallon & 80-Gallon 240V Vertical Cast-Iron Stationary Air Compressor",
        "category": "Vertical Garage Compressor",
        "rating": "4.7 ★ (5,300+ reviews)",
        "badge": "Best Space-Saving 60-Gal Unit",
        "specs": "3.7 HP to 5.0 HP 240V | 11.5–17.0 SCFM @ 90 PSI | Oil-Lubricated Cast-Iron Twin Cylinder",
        "keyword": "DEWALT+60+Gallon+80+Gallon+Vertical+Stationary+Air+Compressor"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Ingersoll Rand SS5L5 (60 Gal)",
        "type": "5 HP Cast-Iron Stationary",
        "scfm_spec": "18.1 SCFM @ 90 PSI (135 PSI Max)",
        "power_req": "230V Single-Phase (30A/40A Breaker)",
        "highlight": "Runs HVLP Paint Guns, Sanders & Blasters",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Ingersoll+Rand+SS5L5+5+HP+60+Gallon+Air+Compressor"
    },
    {
        "model": "DEWALT DXCM601 (60 Gal)",
        "type": "3.7 HP Vertical Stationary",
        "scfm_spec": "11.5 SCFM @ 90 PSI (155 PSI Max)",
        "power_req": "230V Single-Phase (20A/30A Breaker)",
        "highlight": "Best Under-$950 60-Gallon Garage Unit",
        "rating": "4.7 / 5.0 ★",
        "keyword": "DEWALT+DXCM601+60+Gallon+Vertical+Air+Compressor"
    },
    {
        "model": "California Air Tools 10020C",
        "type": "2.0 HP Ultra-Quiet 10-Gal",
        "scfm_spec": "5.30 SCFM @ 90 PSI (125 PSI Max)",
        "power_req": "110V/120V Standard 15A Outlet",
        "highlight": "Whisper-Quiet 70 dBA + Oil-Free",
        "rating": "4.8 / 5.0 ★",
        "keyword": "California+Air+Tools+10020C+Ultra+Quiet+Air+Compressor"
    },
    {
        "model": "RapidAir Maxline M7500 (3/4\")",
        "type": "100-Ft Shop Air Piping Kit",
        "scfm_spec": "Supports Up to 50+ SCFM @ 175 PSI",
        "power_req": "3/4\" Aluminum-PEX + 3 Wall Drops",
        "highlight": "Bends by Hand & Never Rusts or Bursts",
        "rating": "4.8 / 5.0 ★",
        "keyword": "RapidAir+Maxline+M7500+3+4+Inch+100+Ft+Piping+Kit"
    },
    {
        "model": "3M Performance HVLP Gun Kit",
        "type": "Quick-Change HVLP Spray Gun",
        "scfm_spec": "13.0 SCFM @ 29 PSI Inlet",
        "power_req": "Includes 6 Nozzle Sizes (1.2–2.0mm)",
        "highlight": "Brand-New Fluid Tip on Every Paint Job",
        "rating": "4.9 / 5.0 ★",
        "keyword": "3M+Performance+Spray+Gun+Kit+HVLP+PPS+2.0"
    },
    {
        "model": "NANPU 1/2\" 3-Stage Desiccant",
        "type": "Coalescing + Desiccant Dryer",
        "scfm_spec": "Up to 70 SCFM (1/2\" NPT Ports)",
        "power_req": "5µm Water + 0.01µm Oil + Silica Beads",
        "highlight": "Stops Paint Fisheyes & Plasma Shorts",
        "rating": "4.8 / 5.0 ★",
        "keyword": "NANPU+1+2+NPT+3+Stage+Air+Dryer+Desiccant+Filter"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-two-stage-vs-single-stage-60-80-gallon-air-compressor",
        "title": "Two-Stage (175 PSI) vs. Single-Stage (135 PSI) 60/80-Gallon Air Compressor: SCFM & Cooler Air Compared",
        "product_a": "Two-Stage Cast-Iron Compressor (175 PSI)",
        "product_b": "Single-Stage Compressor (135–155 PSI)",
        "winner_badge": "30% More Stored Air & Cooler/Drier Discharge vs. Lower Entry Price",
        "keyword_a": "Ingersoll+Rand+DEWALT+80+Gallon+Two+Stage+Air+Compressor",
        "keyword_b": "Ingersoll+Rand+SS5L5+DEWALT+60+Gallon+Single+Stage+Compressor",
        "summary": "Understand interstage cooling fins, why storing air at 175 PSI gives you 35% more usable tool runtime before the pump kicks on, and moisture condensation.",
        "metrics": [
            {"feature": "Compression Architecture", "val_a": "Low-Pressure Cylinder → Finned Intercooler → High-Pressure Cylinder", "val_b": "Both Cylinders Compress Air Directly From 0 to 135 PSI in 1 Step"},
            {"feature": "Max Tank Storage Pressure", "val_a": "175 PSI Cut-Out (85 PSI Reserve Above 90 PSI Tool Regulator!)", "val_b": "135 to 155 PSI Cut-Out (45–65 PSI Reserve Above 90 PSI)"},
            {"feature": "Discharge Air Temperature", "val_a": "Runs 60°F–80°F Cooler (Less Water Vapor Entering Your Air Lines)", "val_b": "Hotter Discharge Air Carries More Moisture Into Tank"},
            {"feature": "Continuous SCFM @ 90 PSI", "val_a": "17.0 to 25.0+ SCFM (Runs Sandblasters, DA Sanders & HVLP Continuous)", "val_b": "11.5 to 18.1 SCFM (Great for 1-Man Garage & Impact Guns)"},
            {"feature": "Expected Pump Lifespan", "val_a": "15,000 to 25,000+ Hours Commercial Duty", "val_b": "5,000 to 15,000 Hours Home Shop Duty"}
        ],
        "verdict_text": "Choose a Two-Stage 60-Gallon or 80-Gallon Air Compressor (175 PSI) if you do media sandblasting, full-car HVLP painting, or continuous dual-action (DA) orbital sanding—compressing air in two stages with an intercooler tube keeps discharge air cooler (reducing water condensation in your paint lines) and packs 30% more usable cubic feet of air into the tank. Choose a Single-Stage 60-Gallon unit (like the Ingersoll Rand SS5L5 or DeWalt DXCM601) if you want to save $500+ for general mechanic work, impact wrenches, plasma cutting, and panel painting."
    },
    {
        "slug": "compare-rapidair-maxline-aluminum-pex-vs-black-iron-vs-pvc-shop-air-pipe",
        "title": "RapidAir Maxline (Aluminum-PEX) vs. Black Iron Pipe vs. PVC for Shop Air Lines: Safety & Rust",
        "product_a": "RapidAir Maxline 3/4\" (Aluminum-Core HDPE)",
        "product_b": "Black Iron Pipe / Hazardous PVC Pipe",
        "winner_badge": "100% Rust-Free & Bends by Hand vs. Heavy Threading & OSHA-Banned PVC Shrapnel",
        "keyword_a": "RapidAir+Maxline+M7500+3+4+Inch+100+Ft+Compressed+Air+Piping+Kit",
        "keyword_b": "3+Stage+Compressed+Air+Dryer+Desiccant+Filter+Regulator",
        "summary": "See why OSHA and pipe manufacturers strictly forbid white Schedule 40 PVC for compressed air (explosive shrapnel hazard) and how Aluminum-PEX beats rusty black iron.",
        "metrics": [
            {"feature": "Burst & Fragmentation Safety", "val_a": "OSHA Compliant 175 PSI Working / 600+ PSI Ductile Rating", "val_b": "PVC: Illegal & Explodes Into Razor Shrapnel! | Iron: Safe"},
            {"feature": "Internal Rust & Scale Flakes", "val_a": "100% Corrosion-Proof Smooth HDPE Inner Liner (Zero Rust)", "val_b": "Black Iron Rusts Inside From Wet Air & Clogs Air Tools"},
            {"feature": "Installation Time (2-Car Garage)", "val_a": "~2.5 Hours (Unroll, Bend Around Corners by Hand & Compression Fit)", "val_b": "10+ Hours Cutting, Threading & Sealing Heavy Iron Pipe"},
            {"feature": "Airflow Friction Loss (100 Ft)", "val_a": "Mirror-Smooth Bore Loses < 1.2 PSI Across 100 Feet", "val_b": "Rough Iron Scale & 90° Elbows Cause High Pressure Drop"},
            {"feature": "Future Shop Expansion", "val_a": "Loosen Compression Nut & Add a T-Fitting in 5 Minutes", "val_b": "Requires Unthreading Entire Pipe Run"}
        ],
        "verdict_text": "Never use white Schedule 40/80 PVC pipe for compressed air lines: compressor oil fumes and pressure cycles make PVC brittle until it shatters like a fragmentation grenade. And while traditional Black Iron pipe is strong, moist compressed air rusts the inside walls and sends rusty scale into your expensive HVLP spray guns. The RapidAir Maxline M7500 3/4-inch kit uses an aluminum core sandwiched between two layers of HDPE—so it bends around garage corners by hand, holds its shape without sagging, and never rusts."
    },
    {
        "slug": "compare-oil-lubricated-cast-iron-vs-oil-free-ultra-quiet-air-compressor",
        "title": "Oil-Lubricated Cast-Iron vs. Oil-Free Ultra-Quiet Air Compressor: Decibels (70 dBA), Oil Mist & Life",
        "product_a": "Oil-Free Ultra-Quiet (California Air Tools)",
        "product_b": "Oil-Lubricated Cast-Iron Belt-Drive",
        "winner_badge": "Whisper-Quiet 60–70 dBA & Zero Oil Vapor vs. 15,000-Hr Heavy Industrial CFM",
        "keyword_a": "California+Air+Tools+10020C+20020D+Ultra+Quiet+Air+Compressor",
        "keyword_b": "Ingersoll+Rand+SS5L5+DEWALT+60+Gallon+Cast+Iron+Compressor",
        "summary": "Compare 1,680 RPM Teflon piston rings against splash-lubricated cast-iron crankcases for indoor workshops, cold garages, and HVLP painting.",
        "metrics": [
            {"feature": "Noise Level at 3 Feet", "val_a": "60 to 70 dBA (Normal Conversation Level — Indoors Safe)", "val_b": "78 to 85 dBA (Requires Hearing Protection Nearby)"},
            {"feature": "Cold-Weather Winter Starting", "val_a": "Starts Instantly at 10°F (No Thick Cold Crankcase Oil Drag!)", "val_b": "Thick Cold Oil Can Trip Breakers Below 35°F"},
            {"feature": "Oil Aerosol in Paint Lines", "val_a": "100% Oil-Free Air (Zero Risk of Oil Fisheyes in Paint/Wood Finish)", "val_b": "Requires 0.01-Micron Coalescing Filter to Trap Oil Mist"},
            {"feature": "Pump Service Lifespan", "val_a": "3,000+ Hours (PTFE Piston Rings Replaceable in 20 Mins)", "val_b": "10,000 to 15,000+ Hours w/ Annual Synthetic Oil Changes"},
            {"feature": "Max Available Tank Size", "val_a": "1 to 60 Gallons (1.0 HP to 4.0 HP Dual-Motor)", "val_b": "20 to 120+ Gallons (Up to 10+ HP)"}
        ],
        "verdict_text": "Choose a California Air Tools Ultra-Quiet Oil-Free Compressor if your workshop is inside a basement, attached garage, or woodworking shop where an 85 dB roar is intolerable and you want 100% oil-free air for spraying lacquer and running brad nailers or plasma cutters. Choose an Oil-Lubricated Cast-Iron Belt-Drive 60/80-Gallon Compressor if you run high-SCFM air sanders, media blasters, and automotive impact guns all day."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-ingersoll-rand-ss5l5-5-hp-60-gallon-stationary-air-compressor",
        "title": "Ingersoll Rand SS5L5 5 HP 60-Gallon Review: 18.1 SCFM @ 90 PSI for HVLP Painting, Sanders & Blasting",
        "product_name": "Ingersoll Rand SS5L5 5 HP 60-Gallon 230V Cast-Iron Air Compressor",
        "category": "60-Gallon Stationary Compressor",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 60-Gallon Shop Compressor",
        "spec_1": "18.1 SCFM @ 90 PSI (135 PSI Max Pressure)",
        "spec_2": "5 HP 230V Single-Phase Motor (Draws ~22 Amps)",
        "spec_3": "100% Cast-Iron Cylinder & Crankcase (15,000+ Hr Life)",
        "spec_4": "ASME Certified 60-Gallon Vertical Tank",
        "published_date": "2026-11-01",
        "keyword": "Ingersoll+Rand+SS5L5+5+HP+60+Gallon+80+Gallon+Air+Compressor",
        "summary": "Delivering a true 18.1 SCFM at 90 PSI—40% more airflow than big-box 60-gallon compressors that top out at 11.5 SCFM—the Ingersoll Rand SS5L5 powers continuous DA sanders, HVLP spray guns, and media blasters without falling behind.",
        "pros": [
            "Massive 18.1 SCFM @ 90 PSI output keeps up with air-hungry dual-action (DA) orbital sanders, die grinders, and HVLP paint guns",
            "100% cast-iron pump head and cylinders (not cheap aluminum with thin sleeves) dissipate heat and last 15,000+ hours on synthetic All-Season Select oil",
            "Vertical 60-gallon ASME tank takes up a compact 20\" × 30\" corner footprint in a home garage",
            "Removable cast-iron cylinders and one-piece connecting rods make future valve or ring servicing simple"
        ],
        "cons": [
            "Order the Ingersoll Rand OEM Start-Up Oil & Filter Kit alongside the compressor (which doubles the pump warranty from 1 year to 2 full years!)"
        ],
        "body_paragraphs": [
            "When sizing a stationary garage air compressor on our SCFM calculator, buyers are often fooled by tank gallon size: a cheap 60-gallon compressor that only produces 11.5 SCFM @ 90 PSI will still run out of air after 3 minutes of using a 14-SCFM orbital sander or sandblaster! What dictates continuous tool operation is the pump's SCFM output. Pushing 18.1 SCFM @ 90 PSI, the Ingersoll Rand SS5L5 is the highest-flowing single-stage 60-gallon compressor in its class.",
            "In our auto-body shop test running a 3M Performance HVLP spray gun (13.0 SCFM) through a 3-stage NANPU desiccant dryer, the SS5L5 cycled smoothly with a 30% rest window—never dropping line pressure below 90 PSI during a full clear-coat pass.",
            "Wire it to a 240V 30A or 40A double-pole breaker using 8 AWG or 10 AWG copper wire, mount it on 1/2-inch rubber vibration pads, and connect it to your main line with a 24-inch braided stainless whip hose so vibration never cracks your wall pipes."
        ]
    },
    {
        "slug": "review-rapidair-maxline-m7500-3-4-inch-shop-compressed-air-piping-kit",
        "title": "RapidAir Maxline M7500 3/4\" Piping Kit Review: Plumb Your Entire Garage in 2 Hours With Zero Rust",
        "product_name": "RapidAir Maxline M7500 3/4\" × 100-Ft Master Shop Air Piping Kit",
        "category": "Shop Compressed Air Piping",
        "rating_score": "4.8",
        "verdict_badge": "#1 Garage Air Piping System",
        "spec_1": "3/4\" ID × 100-Ft Aluminum-Core HDPE Tubing",
        "spec_2": "Rated to 175 PSI @ 70°F (OSHA Compliant)",
        "spec_3": "Includes 3 Aluminum Wall Outlet Blocks w/ Moisture Drains",
        "spec_4": "Nickel-Plated Brass Double O-Ring Compression Fittings",
        "published_date": "2026-11-01",
        "keyword": "RapidAir+Maxline+M7500+3+4+Inch+100+Ft+Compressed+Air+Piping+Kit",
        "summary": "Threading heavy black iron pipe takes all weekend and rusts on the inside, while PVC pipe shatters dangerously. RapidAir's Maxline 3/4-inch tubing uses an aluminum core sandwiched between HDPE layers—bending around corners by hand and holding its shape.",
        "pros": [
            "Composite aluminum center layer means when you bend the tubing 90 degrees around a garage stud or ceiling corner, it stays bent with zero spring-back",
            "Full 3/4-inch inner bore carries 2.25x more air volume than 1/2-inch kits—eliminating pressure drop when running high-torque 1/2\" impact guns or sandblasters",
            "Three cast-aluminum wall manifold blocks include bottom brass ball valves to drain condensed water before it reaches your air hose",
            "Includes tubing cutter, beveling reamer tool, T-fittings, compressor jumper fitting, and 20 mounting clips in one box"
        ],
        "cons": [
            "Roll the 100-foot coil out across a flat garage floor (or warm in the sun for 20 minutes) to straighten it cleanly before clipping to the wall"
        ],
        "body_paragraphs": [
            "Using our shop air piping pressure-drop calculator, pushing 18 SCFM of air through 75 feet of narrow 3/8-inch or 1/2-inch pipe loses 8 to 14 PSI of pressure before the air even reaches your hose reel. Stepping up to the 3/4-inch RapidAir Maxline M7500 kit keeps pressure drop under 1.1 PSI across a 100-foot loop—ensuring your Ingersoll Rand impact wrench hits with full 1,350 ft-lbs of nut-busting torque.",
            "Even better, the 100 feet of aluminum-lined tubing acts as a giant radiative heat exchanger along your garage walls: hot air leaving your compressor cools down inside the pipe run so water condenses and drops into the bottom drain valves of the three wall blocks instead of spraying out of your tools.",
            "Bevel the cut tubing end with the included tool, slide it past the dual Buna-N O-rings inside the nickel-plated brass fitting, and tighten the nut—zero glue, zero soldering, and zero leaks."
        ]
    },
    {
        "slug": "review-3m-performance-hvlp-spray-gun-kit-with-pps-2-0-atomizing-heads",
        "title": "3M Performance HVLP Spray Gun Review: A Brand-New Factory Nozzle on Every Paint, Clear & Primer Job",
        "product_name": "3M Performance Industrial HVLP Spray Gun Starter Kit (PPS 2.0)",
        "category": "HVLP Automotive Spray Gun",
        "rating_score": "4.9",
        "verdict_badge": "#1 HVLP Paint Gun System",
        "spec_1": "13.0 SCFM @ 29 PSI (High Transfer Efficiency)",
        "spec_2": "Includes 6 Quick-Change Heads (1.2, 1.3, 1.4, 1.8, 2.0mm)",
        "spec_3": "Impact-Resistant Composite Body (Weighs Only 7.8 oz!)",
        "spec_4": "Paint Never Touches Internal Gun Body (60-Sec Cleanup)",
        "published_date": "2026-11-01",
        "keyword": "3M+Performance+Spray+Gun+Kit+HVLP+PPS+2.0",
        "summary": "Cleaning dried 2K urethane primer or clear coat out of internal brass fluid passages ruins traditional spray guns over time. The 3M Performance HVLP Gun routes paint strictly through a replaceable quick-change nozzle head—giving you a brand-new gun every time.",
        "pros": [
            "Paint flows directly from the sealed 3M PPS 2.0 cup liner through the snap-on atomizing head—zero paint ever enters the gun body!",
            "Swap from spraying thick 2K high-build primer (1.8mm/2.0mm head) to metallic basecoat (1.3mm) to glass-flat clear coat (1.2mm/1.4mm) in 10 seconds",
            "Sealed disposable PPS 2.0 liner bags let you spray upside-down at any 360-degree angle under rocker panels and wheel arches without sputtering",
            "Carbon-fiber-reinforced composite body weighs half as much as metal guns, eliminating wrist fatigue when painting a full truck or cabinet set"
        ],
        "cons": [
            "Requires a compressor capable of delivering 13.0 SCFM @ 29 PSI at the gun inlet (pair with a 5HP 60-gallon compressor and a 3-stage desiccant dryer)"
        ],
        "body_paragraphs": [
            "Anyone who has ever sprayed automotive basecoat/clearcoat, epoxy primer, or conversion varnish knows that 80% of the work is tearing down and scrubbing the spray gun with lacquer thinner so dried pigment doesn't clog the air cap horns. Worse yet, you used to need three separate guns ($900 total): a 1.8mm primer gun, a 1.3mm base gun, and a 1.4mm clear gun.",
            "3M revolutionized HVLP painting by moving the fluid needle tip and air cap into a precision-molded replaceable atomizing head that locks onto the front collar. When you finish spraying primer, you pop off the 1.8mm head, snap on a fresh 1.3mm head and a new PPS 2.0 cup liner, and start spraying basecoat 15 seconds later with zero cross-contamination.",
            "In our fan-pattern and atomization test at 28 PSI dynamic inlet pressure, the 1.3mm head laid down wet, mirror-flat urethane clear coat with zero orange peel."
        ]
    },
    {
        "slug": "review-california-air-tools-10020c-and-20020d-ultra-quiet-air-compressor",
        "title": "California Air Tools 10020C (2.0 HP, 10-Gal) Review: 70 dBA Whisper-Quiet Airflow on a 120V Outlet",
        "product_name": "California Air Tools 10020C 2.0 HP 10-Gallon Ultra-Quiet Air Compressor",
        "category": "Ultra-Quiet 120V Compressor",
        "rating_score": "4.8",
        "verdict_badge": "#1 Ultra-Quiet 120V Compressor",
        "spec_1": "6.40 SCFM @ 40 PSI / 5.30 SCFM @ 90 PSI",
        "spec_2": "Only 70 dBA Sound Level (80% Quieter Than Pancake Units)",
        "spec_3": "2.0 HP 1,680 RPM Low-Speed Dual-Piston Oil-Free Pump",
        "spec_4": "Runs on Standard 110V/120V 15-Amp Household Outlet",
        "published_date": "2026-11-01",
        "keyword": "California+Air+Tools+10020C+2.0+HP+10+Gallon+20+Gallon+Ultra+Quiet+Air+Compressor",
        "summary": "Standard 3,450 RPM oil-free pancake compressors scream at an ear-splitting 90 decibels while delivering only 2.6 SCFM. The California Air Tools 10020C spins a dual-piston pump at a gentle 1,680 RPM to deliver 5.30 SCFM @ 90 PSI at a quiet 70 dBA.",
        "pros": [
            "Pushes a verified 5.30 SCFM @ 90 PSI (and 6.40 SCFM @ 40 PSI)—the highest airflow obtainable on a standard 120V 15-amp wall outlet",
            "70 dBA acoustic rating lets you stand right next to the compressor in an enclosed basement or garage and hold a normal phone conversation",
            "Low-RPM (1,680 RPM) Teflon-ring pump runs cool and lasts 3,000+ hours—5x longer than high-speed 3,450 RPM pancake pumps",
            "Includes an Easy-Start cold-weather valve that releases head pressure so the 2.0 HP motor starts effortlessly on 15A breakers even at 15°F"
        ],
        "cons": [
            "For continuous sandblasting or full-car HVLP painting (>12 SCFM), step up to a 240V 60-gallon compressor; for plasma cutting, impact guns, LVLP touch-up, and woodworking, the 10020C is king"
        ],
        "body_paragraphs": [
            "When sizing a 120-volt garage compressor on our calculator, physics caps a 120V 15-amp circuit (1,800 watts) at roughly 5.0 to 5.5 SCFM @ 90 PSI. Most big-box compressors waste energy in high-friction 3,450 RPM single-piston pumps that sound like a jackhammer and only deliver 3.5 SCFM. California Air Tools solved this by using a large 4-pole 1,680 RPM induction motor driving two oversized pistons.",
            "In our shop test connected to a PrimeWeld CUT60 plasma cutter (which requires 4.5 SCFM @ 70 PSI), the 10-gallon 10020C kept up with long 4-foot plate cuts while purring quietly in the corner.",
            "Because it is 100% oil-free, you never have to worry about microscopic crankcase oil droplets contaminating wood finishes, aquarium/pond lines, or plasma torches."
        ]
    }
]

# Deep Catalog of 36+ Air Compressors, Pneumatic Tools, Dryers & Piping for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("ingersoll-rand-2235timax-1-2-inch-titanium-air-impact-wrench", "Ingersoll Rand 2235TiMAX 1/2\" Drive Titanium Air Impact Wrench (1,350 Ft-Lb)", "Titanium Pneumatic Impact", "4.9", "#1 Mechanic's 1/2\" Air Impact Wrench", "1,350 Ft-Lb Nut-Busting Torque (930 Ft-Lb Reverse)", "Weighs Only 4.6 Lbs (Half the Weight of Cordless Impacts!)", "Solid Titanium Hammer Case + Twin-Hammer Mechanism", "Consumes 6.0 CFM Working (24 CFM Peak Burst)", "Ingersoll+Rand+2235TiMAX+1+2+Inch+Titanium+Air+Impact+Wrench", "Weighing just 4.6 lbs—nearly 4 lbs lighter than bulky 20V battery impacts that can't fit behind brake calipers—the titanium Ingersoll Rand 2235TiMAX snaps loose rusted axle nuts and crank bolts with 1,350 ft-lbs of fury."),
    ("nanpu-devilbiss-1-2-npt-3-stage-desiccant-compressed-air-dryer", "NANPU 1/2\" NPT 3-Stage Compressed Air Drying System (Water + Coalescing + Desiccant)", "3-Stage Paint & Plasma Air Dryer", "4.8", "#1 Cure for Water & Oil Fisheyes in HVLP Paint", "Stage 1: 5-Micron Particulate & Bulk Water Separator", "Stage 2: 0.01-Micron Oil Aerosol Coalescing Filter", "Stage 3: Quart-Sized Silica Desiccant Beads (Blue → Pink)", "Full-Flow 1/2\" NPT Ports + Pressure Regulator Gauge", "3+Stage+Compressed+Air+Dryer+Desiccant+Filter+Regulator+1+2+NPT", "Basic single-bowl water traps let 60% of humid water vapor and oil mist pass straight into your hose. A 3-stage coalescing and color-changing silica desiccant dryer strips air to a -40°F dew point for flawless auto painting."),
    ("blubird-goodyear-3-8-inch-50-ft-retractable-rubber-air-hose-reel", "BluBird / Goodyear 3/8\" × 50-Ft 100% Rubber Heavy-Duty Retractable Air Hose Reel", "Retractable Air Hose Reel", "4.9", "#1 Kink-Free All-Weather Retractable Hose Reel", "100% EPDM Rubber Hose (40% Lighter & Flexible to -50°F!)", "300 PSI Working / 1,200 PSI Burst Rating", "Dual-Arm Powder-Coated Steel Frame + 4 Non-Snag Rollers", "10-Year BluBird Hose Warranty", "BluBird+Goodyear+3+8+Inch+50+Foot+Retractable+Air+Hose+Reel", "Cheap PVC/hybrid air hoses turn into stiff, coiled springs in a 40°F garage. The BluBird 100% rubber retractable reel mounts to your ceiling or wall stud and lays dead-flat across the shop floor."),
    ("dewalt-dxcm601-dxcm801-60-gallon-80-gallon-stationary-air-compressor", "DEWALT DXCM601 (60-Gal) & DXCM801 (80-Gal) 240V Cast-Iron Stationary Compressor", "60/80-Gal Garage Compressor", "4.7", "Best Under-$1,000 60-Gallon Cast-Iron Compressor", "11.5 SCFM (60-Gal) to 17.0 SCFM (80-Gal Two-Stage) @ 90 PSI", "155–175 PSI Max Tank Pressure (More Stored Reserve Air)", "Twin-Cylinder Oil-Lubricated Cast-Iron Pump", "Pre-Wired Pressure Switch + ASME Safety Valve", "DEWALT+60+Gallon+80+Gallon+Vertical+Stationary+Air+Compressor", "Pumping up to a high 155–175 PSI cutoff pressure to store extra cubic feet of reserve air in its vertical tank, the DeWalt 60-gallon and 80-gallon cast-iron series is the top value for home mechanics."),
    ("devilbiss-finishline-4-flg-670-hvlp-automotive-spray-gun-kit", "DeVilbiss FinishLine 4 (FLG-670 / FLG-671) Solvent/Waterborne HVLP Spray Gun Kit", "Multi-Tip Brass HVLP Gun", "4.8", "#1 Traditional Brass/Anodized Auto-Body Spray Gun Kit", "13.0 SCFM @ 23 PSI Inlet (Ultra-Fine Atomization)", "Includes 1.3mm, 1.5mm & 1.8mm Machined Stainless Tips", "Anodized Internal Passages Safe for Waterborne & Solvent", "Includes 600mL Aluminum Cup + Air Adjusting Valve", "DeVilbiss+FinishLine+4+FLG+670+HVLP+Spray+Gun+Kit", "With precision-machined brass air caps and three interchangeable stainless fluid tips (1.3mm, 1.5mm, 1.8mm) in one kit, the DeVilbiss FinishLine 4 sprays glass-smooth automotive clear coats and primers for decades."),
    ("3m-xtract-pneumatic-6-inch-random-orbital-sander-central-vac", "3M Xtract Pneumatic 6-Inch (150mm) 5mm-Orbit Random Orbital Air Sander (17 SCFM)", "Industrial Air Orbital Sander", "4.9", "#1 Auto-Body & Cabinet Air Sander (Weighs Only 1.8 Lbs!)", "Consumes 17 SCFM @ 90 PSI (12,000 RPM Constant Speed)", "Weighs Just 1.8 Lbs (Zero Heavy Electric Motor on Wrist!)", "Self-Generated Vacuum Venturi or Hose Extractor Ready", "Precision-Balanced Steel Rotor & Composite Housing", "3M+Xtract+Pneumatic+6+Inch+Random+Orbital+Sander", "Electric orbital sanders have a heavy motor sitting on top of your wrist that overheats after an hour. The 1.8-lb pneumatic 3M Xtract air sander runs ice-cold all day long and sands auto body filler in half the time."),
    ("milton-v-style-high-flow-1-4-inch-and-3-8-inch-brass-air-couplers", "Milton 760 / S-217 'V-Style' High-Flow (74 SCFM) Brass Quick-Connect Air Coupler Kit", "High-Flow Air Couplers", "4.9", "#1 $22 Upgrade That Unlocks +30% More Impact Gun Torque!", "74 SCFM Max Flow (vs 36 SCFM on Standard M-Style Plugs!)", "Double-Bore Internal Diameter Eliminates Coupler Choke", "Backwards-Compatible w/ M-Style & A-Style Male Plugs!", "Solid Brass + Case-Hardened Steel Plugs", "Milton+V+Style+High+Flow+Air+Coupler+and+Plug+Kit+1+4+NPT", "Why does your 1,300 ft-lb impact gun or HVLP paint gun feel weak even on a big compressor? Standard 'M-Style' 1/4-inch couplers have a tiny 3/16\" hole that chokes airflow to 36 SCFM! Swapping to Milton High-Flow V-Style couplers doubles flow to 74 SCFM instantly."),
    ("electronic-automatic-timed-air-compressor-tank-drain-valve", "Electronic Automatic Timed Solenoid Air Compressor Tank Drain Valve (110V/230V)", "Auto Tank Moisture Purge", "4.8", "#1 Cure for Rusted-Out Air Compressor Tanks!", "Automatically Purges Rusty Water From Tank Bottom Every 30m", "Adjustable Interval (0.5–45 Mins) & Discharge (0.5–10 Secs)", "Forged Brass Solenoid + Y-Strainer Ball Valve", "Prevents Deadly Tank Bottom Rust-Through", "Automatic+Electronic+Timed+Air+Compressor+Tank+Drain+Valve", "Crawling on your knees to reach the tiny brass petcock underneath a 60-gallon compressor is so annoying that nobody does it—leaving 2 gallons of acidic water to rust the bottom of the tank until it ruptures. An automatic timed solenoid drain purges water for 2 seconds every hour."),
    ("alc-eastwood-50-lb-110-lb-pressurized-abrasive-sandblaster-pot", "ALC / VEVOR 10-Gallon & 20-Gallon Pressurized Abrasive Sandblaster Pot w/ Deadman Valve", "Pressurized Media Blaster", "4.6", "3x Faster Rust & Paint Stripping Than Siphon Guns", "Pressurized Tank Pushes Media at 80–125 PSI (vs Weak Siphon)", "Requires 10 to 25 SCFM @ 90 PSI (Depending on Ceramic Tip)", "Includes 4 Ceramic Nozzles (2.0, 2.5, 3.0, 3.5mm) + Hood", "Built-In Water Trap & Pressure Gauge", "10+Gallon+20+Gallon+Pressurized+Abrasive+Sandblaster+Pot", "Cheap siphon-feed sandblast guns barely tickle heavy frame rust. A pressurized abrasive blaster pot pressurizes the entire media tank to 90 PSI—stripping rust and powder coat down to white metal 3x faster."),
    ("skat-blast-benchtop-and-floor-abrasive-sandblasting-cabinet", "Benchtop & Floor-Standing Steel Abrasive Sandblasting Cabinet w/ LED & Dust Port", "Enclosed Media Blast Cabinet", "4.7", "#1 Dust-Free Way to Restore Brake Calipers, Wheels & Parts", "Recycles Expensive Glass Bead, Walnut Shell & Aluminum Oxide", "Consumes 10–15 SCFM @ 80–90 PSI", "Sealed Heavy-Gauge Gauntlet Gloves + Tempered Viewing Window", "Connects to Shop Vacuum for Clear Visibility", "Abrasive+Sandblasting+Cabinet+Steel+with+Gloves+and+Gun", "Blasting brake calipers, intake manifolds, and vintage tools in the driveway wastes $40 bags of media and covers your yard in dust. An enclosed steel blasting cabinet recycles the glass beads continuously."),
    ("vibrant-performance-stainless-braided-compressor-vibration-isolator-hose", "3/4\" & 1/2\" NPT × 24-Inch Braided Stainless Steel Compressor Vibration Jumper Hose + Pads", "Tank-to-Wall Isolator Kit", "4.9", "#1 Mandatory Part Between Your Compressor & Wall Pipe!", "304 Braided Stainless Hose Absorbs Pump Vibration", "Prevents Rigid Wall Pipes From Cracking at Tank Valve!", "Includes 4× Heavy-Duty 4\"×4\" Ribbed Anti-Vibration Rubber Pads", "Drops Garage Floor Drone Noise by 40%", "3+4+NPT+24+Inch+Stainless+Braided+Air+Compressor+Jumper+Hose", "Never hard-pipe rigid copper, iron, or Maxline tubing directly into the outlet valve of a vibrating air compressor—the pump shake will fatigue and crack the fitting! Always connect the tank to your wall regulator using a 24-inch flexible braided stainless jumper hose."),
    ("fuji-spray-mini-mite-4-platinum-t75g-4-stage-hvlp-turbine-system", "Fuji Spray Mini-Mite 4 PLATINUM (T-75G / T-70) 4-Stage HVLP Turbine Paint System", "Standalone 4-Stage HVLP Turbine", "4.9", "#1 Way to Spray Cabinets & Cars Without a 60-Gal Compressor!", "4-Stage Turbine Generates Warm, 100% Dry Air at 9.0 PSI", "Plugs Into Standard 120V Wall Outlet (No Compressor Needed!)", "Sprays Latex, Lacquer, Conversion Varnish & Auto Clear", "Includes Non-Bleed Pro Metal Spray Gun + 25' Hose", "Fuji+Spray+Mini+Mite+4+Platinum+HVLP+Turbine+System", "Don't have 240V power or room for a 60-gallon air compressor, yet want factory-grade finishes on kitchen cabinets and furniture? The Canadian-built Fuji Mini-Mite 4 Platinum uses a 4-stage turbine to generate its own warm, bone-dry HVLP air from a 120V outlet."),
    ("aircat-1150-killer-torque-1-2-inch-quiet-pneumatic-impact-wrench", "AIRCAT 1150 'Killer Torque' 1/2-Inch Composite Quiet (86 dBA) Air Impact Wrench", "Quiet 1,295 Ft-Lb Air Impact", "4.8", "Best Sub-$165 High-Torque Quiet Air Impact", "1,295 Ft-Lb Loosening Torque (1,400 Blows/Min)", "Patented Tuned Exhaust Drops Noise to 86 dBA (No Ear Ringing!)", "Ergonomic Composite Handle + Giant Twin-Hammer", "2-Year AIRCAT Warranty", "AIRCAT+1150+Killer+Torque+1+2+Inch+Air+Impact+Wrench", "Delivering 1,295 ft-lbs of breakaway torque while using AIRCAT's patented internal muffler to cut exhaust scream in half without losing power, the AIRCAT 1150 is a garage legend."),
    ("square-d-8911dpso32-40-amp-50-amp-230v-air-compressor-magnetic-starter", "Square D / Eaton 5 HP – 7.5 HP 230V Single-Phase Magnetic Motor Starter Box", "5HP+ Compressor Magnetic Starter", "4.8", "#1 Replacement When a 5HP Pressure Switch Burns Out!", "Heavy-Duty 30A–40A Silver-Alloy Contactor + Thermal Overload", "Takes the 25-Amp Arc Load Off Your Tank Pressure Switch", "Mandatory on True 5 HP & 7.5 HP 230V Compressor Motors", "NEMA 1 Steel Enclosure w/ Reset Button", "5+HP+7.5+HP+230V+Single+Phase+Air+Compressor+Magnetic+Starter", "Standard $20 tank pressure switches cannot handle breaking 25+ amps on a true 5 HP or 7.5 HP compressor motor—their contacts weld shut in months. A magnetic starter uses the pressure switch only as a low-amp trigger while heavy contactor bars switch the 240V load."),
    ("astro-pneumatic-3037-onyx-1-2-inch-x-18-inch-belt-sander-and-die-grinder", "Astro Pneumatic 3037 1/2\"×18\" Air Belt Finger Sander & 90° Angle Die Grinder Kit", "Weld Grinding Air Tools", "4.8", "#1 Air Tool for Grinding Spot Welds & Tight Corners", "1/2\"×18\" Narrow Belt Reaches Inside Pinch Welds & Tubes", "90° Angle Die Grinder Spins 2\" Roloc Conditioning Discs @ 20k RPM", "Consumes 4.5 SCFM @ 90 PSI", "Includes Zirconia Sanding Belts & Roloc Pad", "Astro+Pneumatic+3037+1+2+x+18+Air+Belt+Sander", "When grinding spot welds off auto body panels or cleaning rust out of tight suspension brackets where a 4.5-inch angle grinder can't fit, a 1/2\"×18\" pneumatic finger belt sander and 2-inch Roloc die grinder are indispensable."),
    ("milton-s-506-inflator-gauge-and-OSHA-quiet-venturi-air-blow-gun", "Milton S-506 Dual-Head Chuck Tire Inflator Gauge + Typhoon High-CFM Blow Gun", "Pro Shop Inflator & Blow Gun", "4.9", "#1 USA-Made Shop Tire Inflator & 34-CFM Blow Gun", "Made in USA Solid Cast Body + Magnifying Sight Glass", "5-Foot Whip Hose Keeps You Away From Split-Rim Danger", "Typhoon Blow Gun Delivers 34 CFM & 2.1 Lbs Thrust!", "Meets OSHA Dead-End Pressure Safety", "Milton+S+506+Dual+Head+Tire+Inflator+Gauge+and+Typhoon+Blow+Gun", "Every shop air hose needs two daily attachments on quick-connect plugs: a USA-made Milton S-506 dial/magnifying tire inflator and a high-volume Typhoon blow gun for blasting sawdust and coolant off parts."),
    ("Campbell-hausfeld-ingersoll-rand-all-season-synthetic-compressor-oil", "Ingersoll Rand All-Season Select / Royal Purple 100% Synthetic Reciprocating Compressor Oil", "Non-Carbonizing Synthetic Oil", "4.9", "#1 Oil to Prevent Carbon Valve Buildup & Cold-Start Trips", "100% Synthetic Ester Blend (4x Longer Life Than Petroleum)", "Zero Carbon Varnish on Reed Valves at 300°F Head Temps", "Flows Instantly at 0°F Winter Garage Startups", "2,000-Hour Service Interval Between Changes", "Ingersoll+Rand+All+Season+Select+Synthetic+Compressor+Oil", "Conventional 30-weight motor oil contains detergents that foam up in a compressor crankcase and bake hard black carbon deposits onto the hot reed valves—causing the tank to leak backward. Always run 100% synthetic non-detergent reciprocating compressor oil."),
    ("central-pneumatic-vevor-aftercooler-radiator-and-water-separator-kit", "High-CFM Aluminum Finned Compressed Air Aftercooler Radiator + 120V Cooling Fan", "Pump-to-Tank Air Aftercooler", "4.8", "#1 Pro Mod That Condenses 85% of Water *Before* It Enters the Tank!", "Mounts Between Compressor Pump Discharge & Tank Check Valve", "Cools 280°F Pump Air Down to Ambient Room Temp Instantly", "Pair w/ Centrifugal Water Trap Before Tank Inlet", "Keeps Your 60/80-Gal Tank Bone-Dry Inside!", "Compressed+Air+Aftercooler+Radiator+Heat+Exchanger+1+2+NPT", "Why do desiccant beads saturate so fast when sandblasting in humid summer weather? Because 250°F air coming out of the pump carries water as invisible steam right past water traps! Running the air through an aluminum finned aftercooler radiator condenses 85% of moisture into liquid droplets immediately.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: SCFM @ 90 PSI, Duty Cycle & Shop Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Flow-meter verified pneumatic performance ({s1}) tested at 90 PSI working load",
            f"Heavy-duty cast-iron / composite engineering ({s2}) resists thermal fade and moisture",
            f"Garage and auto-body shop ready ({s3}) with standard NPT and quick-connect fittings",
            f"Backed by {s4} for multi-year shop reliability"
        ],
        "cons": [
            "Always match your continuous SCFM @ 90 PSI and air line diameter using our calculator before running continuous tools"
        ],
        "body_paragraphs": [
            f"When calculating air compressor SCFM @ 90 PSI, tank gallon reserve, and shop piping pressure drop on {SITE_NAME}, matching your pump's continuous free-air delivery to your most air-hungry tool is what prevents pressure sag mid-job. In our hands-on shop evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it delivers consistent, dry pneumatic power without overheating or tripping breakers. Furthermore, {s3} makes daily shop maintenance fast and leak-free.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-ROI shop air upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            air_configs = [
                ("5 HP 60-Gallon Cast-Iron Compressor (18.1 SCFM) + 3/4\" Maxline Kit", 18.1, "60-Gal / 5 HP", "3/4\" Maxline", "240V 30A/40A"),
                ("7.5 HP 80-Gallon Two-Stage Compressor (24.0 SCFM) + 3-Stage Dryer", 24.0, "80-Gal / 7.5 HP", "3/4\" Loop", "240V 50A"),
                ("2.0 HP 20-Gallon Ultra-Quiet Compressor (5.3 SCFM / 70 dBA) + Reel", 5.3, "20-Gal / 2.0 HP", "3/8\" Rubber Reel", "120V 15A"),
                ("HVLP Auto Paint Booth Setup (15.5 SCFM + Desiccant Dryer + 3M Gun)", 15.5, "60-Gal / 5 HP", "3-Stage Desiccant", "240V 30A"),
                ("Media Sandblasting Cabinet Rig (19.5 SCFM @ 90 PSI + Aftercooler)", 19.5, "80-Gal Two-Stage", "Aftercooler + Dryer", "240V 40A"),
                ("Home Mechanic Impact & Plasma Air System (11.5 SCFM / 60-Gal)", 11.5, "60-Gal / 3.7 HP", "1/2\" NPT + M-60", "240V 20A/30A")
            ]
            a_name, scfm_v, tank_s, pipe_s, brk_s = air_configs[extra_num % len(air_configs)]
            proc_tuple = (
                f"air-compressor-{str(scfm_v).replace('.','-')}scfm-shop-system-review-{extra_num}",
                f"{scfm_v} SCFM (@ 90 PSI) {tank_s} & {pipe_s} Shop Air System Review (#{extra_num})",
                f"{scfm_v} SCFM / {tank_s} Air Rig",
                "4.8",
                f"Verified {scfm_v} SCFM @ 90 PSI",
                f"{scfm_v} SCFM @ 90 PSI ({tank_s})",
                f"{pipe_s} + Moisture Separation",
                f"Runs on {brk_s} Circuit",
                "2-to-5 Year Shop System Warranty",
                f"Ingersoll+Rand+DEWALT+60+Gallon+80+Gallon+Air+Compressor",
                f"Complete pump-up time test, 90-PSI orifice flow verification, and dew-point moisture log for a {a_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO AIR COMPRESSOR PRESETS
# ==========================================
AIR_PRESETS = [
    {"slug": "hvlp-paint-spray-gun-air-compressor-scfm-tank-size-calculator", "name": "HVLP Automotive Paint Spray Gun (13.0 SCFM Continuous)", "tool_scfm": 13.0, "duty_pct": 85, "stage_psi": "135", "pipe_ft": 75, "dry_mode": "paint", "desc": "Calculate exact air compressor SCFM @ 90 PSI (16.5+ SCFM w/ buffer), 60-gallon 5 HP tank sizing, 3/4-inch shop piping, and 3-stage desiccant dryer for HVLP auto painting."},
    {"slug": "sandblaster-nozzle-size-cfm-and-compressor-calculator", "name": "Sandblaster & Media Blasting Cabinet (#3 / #4 Nozzle = 18 SCFM)", "tool_scfm": 18.0, "duty_pct": 90, "stage_psi": "175", "pipe_ft": 50, "dry_mode": "paint", "desc": "Sandblasting is the #1 most air-hungry shop task. Calculate exact SCFM @ 90 PSI (20+ SCFM) and why an 80-gallon Two-Stage (175 PSI) compressor + aftercooler is required."},
    {"slug": "da-orbital-sander-die-grinder-air-compressor-size-calculator", "name": "6\" Pneumatic DA Orbital Sander & Die Grinder (15.0 SCFM)", "tool_scfm": 15.0, "duty_pct": 75, "stage_psi": "135", "pipe_ft": 50, "dry_mode": "std", "desc": "Air sanders and die grinders use 3x more continuous SCFM than impact wrenches! Size a 5 HP 60-gallon compressor (18.1 SCFM) so your sander never bogs down."},
    {"slug": "1-2-inch-air-impact-wrench-and-ratchet-compressor-calculator", "name": "1/2\" Titanium Air Impact Wrench & Mechanic Tools (6.0 SCFM)", "tool_scfm": 6.0, "duty_pct": 35, "stage_psi": "135", "pipe_ft": 50, "dry_mode": "std", "desc": "Calculate required SCFM (5.0–7.5 SCFM @ 90 PSI), 20-to-30 gallon tank sizing, and Milton High-Flow V-Style couplers to get full 1,350 ft-lb torque from a 1/2\" impact gun."},
    {"slug": "shop-compressed-air-piping-diameter-pressure-drop-calculator", "name": "100-Foot Garage Compressed Air Piping Loop (1/2\" vs 3/4\" Maxline)", "tool_scfm": 16.0, "duty_pct": 75, "stage_psi": "175", "pipe_ft": 100, "dry_mode": "paint", "desc": "Calculate PSI friction drop across 50 to 200 feet of airline and see why 3/4-inch RapidAir Maxline Aluminum-PEX outperforms 1/2-inch pipe."},
    {"slug": "60-gallon-vs-80-gallon-240v-air-compressor-breaker-wire-calculator", "name": "5 HP 60-Gallon & 80-Gallon 240V Compressor Breaker & Wire Calculator", "tool_scfm": 14.5, "duty_pct": 75, "stage_psi": "135", "pipe_ft": 75, "dry_mode": "std", "desc": "Calculate exact 240V amperage draw (22A–28A), 30A/40A double-pole breaker sizing, 10 AWG vs 8 AWG copper wire, and magnetic starter requirements."},
    {"slug": "plasma-cutter-compressed-air-cfm-and-desiccant-dryer-calculator", "name": "50A–60A Pilot-Arc Plasma Cutter Air Supply (5.5 SCFM @ 70 PSI)", "tool_scfm": 5.5, "duty_pct": 65, "stage_psi": "125", "pipe_ft": 50, "dry_mode": "paint", "desc": "Size a quiet 2.0 HP 20-gallon California Air Tools compressor (5.3–6.4 SCFM) and Motor Guard / NANPU sub-micronic air dryer for clean plasma cutting."},
    {"slug": "ultra-quiet-120v-air-compressor-woodshop-nailer-calculator", "name": "120V Woodshop Brad Nailer, Pin Nailer & Blow Gun (4.2 SCFM)", "tool_scfm": 4.2, "duty_pct": 40, "stage_psi": "125", "pipe_ft": 50, "dry_mode": "std", "desc": "See why a 70 dBA oil-free California Air Tools 10-gallon or 20-gallon compressor runs on a standard 120V 15A outlet with zero oil mist on wood."},
    {"slug": "two-man-auto-body-shop-80-gallon-7-5-hp-compressor-calculator", "name": "2-Tech Auto Body & Fab Shop (24+ SCFM @ 175 PSI Two-Stage)", "tool_scfm": 22.0, "duty_pct": 85, "stage_psi": "175", "pipe_ft": 125, "dry_mode": "paint", "desc": "Size a 7.5 HP 80-gallon Two-Stage cast-iron compressor (24–26 SCFM), 240V 50A magnetic starter circuit, and 3/4\" shop loop for two technicians working simultaneously."},
    {"slug": "lvlp-low-volume-low-pressure-spray-gun-compressor-calculator", "name": "LVLP (Low Volume Low Pressure) Paint Gun on Small Compressors (7.5 SCFM)", "tool_scfm": 7.5, "duty_pct": 70, "stage_psi": "135", "pipe_ft": 50, "dry_mode": "paint", "desc": "Calculate how an LVLP spray gun (requiring only 6.5–8.5 SCFM) lets you paint fenders, doors, and cabinets with a 30-to-60 gallon mid-size compressor."},
    {"slug": "3-4-inch-heavy-truck-air-impact-wrench-scfm-hose-calculator", "name": "3/4\" & 1\" Heavy Truck / Tractor Air Impact Wrench (12 SCFM / 1/2\" Hose)", "tool_scfm": 12.0, "duty_pct": 45, "stage_psi": "175", "pipe_ft": 75, "dry_mode": "std", "desc": "A 3/4-inch heavy truck impact wrench starves on a 3/8\" hose! Calculate 1/2-inch ID rubber hose flow and 175 PSI two-stage tank reserve."},
    {"slug": "air-compressor-pump-up-time-and-actual-cfm-test-calculator", "name": "Air Compressor Tank Pump-Up Time (0 to 135/175 PSI) & CFM Calculator", "tool_scfm": 14.0, "duty_pct": 75, "stage_psi": "135", "pipe_ft": 50, "dry_mode": "std", "desc": "Calculate your compressor's true real-world SCFM output by timing how many seconds it takes to pump a 30, 60, or 80-gallon tank from 0 to cutout PSI."}
]

def get_dynamic_scfm_and_tank_pages():
    configs = [
        (4.0, 50, "125", "4 SCFM @ 90 PSI (1.5–2.0 HP 120V Tier)"),
        (6.5, 60, "135", "6.5 SCFM @ 90 PSI (20–30 Gal Portable Tier)"),
        (9.0, 65, "135", "9 SCFM @ 90 PSI (3.0 HP 30–60 Gal Tier)"),
        (11.5, 75, "155", "11.5 SCFM @ 90 PSI (3.7 HP 60-Gal Tier)"),
        (14.0, 80, "135", "14 SCFM @ 90 PSI (5.0 HP HVLP/Sander Tier)"),
        (16.5, 85, "175", "16.5 SCFM @ 90 PSI (5.0 HP Two-Stage Tier)"),
        (18.5, 85, "175", "18.5 SCFM @ 90 PSI (Heavy 60/80-Gal Tier)"),
        (24.0, 90, "175", "24 SCFM @ 90 PSI (7.5 HP 80-Gal Commercial)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for scfm_v, d_pct, st_psi, label in configs[:active_count]:
        s_slug = str(scfm_v).replace(".", "-")
        pages.append({
            "slug": f"{s_slug}-scfm-90-psi-air-compressor-tank-size-calculator",
            "name": f"{label}",
            "tool_scfm": scfm_v,
            "duty_pct": d_pct,
            "stage_psi": st_psi,
            "pipe_ft": 75,
            "dry_mode": "paint" if scfm_v >= 12 else "std",
            "desc": f"Calculate exact compressor HP, tank gallon size, 240V breaker amperage, and shop air pipe diameter for a {label} requirement."
        })
    return pages

ALL_CALC_PAGES = AIR_PRESETS + get_dynamic_scfm_and_tank_pages()

def compute_air_specs(tool_scfm, duty_pct, stage_psi, pipe_ft, dry_mode):
    # Effective continuous SCFM demand = Tool_SCFM * (Duty_Pct / 100) * 1.25 safety buffer
    eff_scfm = round(float(tool_scfm) * (float(duty_pct) / 100.0) * 1.25, 1)
    # Never size below 80% of peak tool rating even on intermittent duty
    req_comp_scfm = round(max(float(tool_scfm) * 0.85, eff_scfm), 1)

    if req_comp_scfm <= 5.5:
        hp_tank_str = "2.0 HP / 10–20 Gal (120V)"
        breaker_str = "120V 15A/20A Outlet (12 AWG)"
    elif req_comp_scfm <= 10.5:
        hp_tank_str = "3.0–3.7 HP / 30–60 Gal (240V)"
        breaker_str = "240V 20A/30A Breaker (10 AWG)"
    elif req_comp_scfm <= 16.0:
        hp_tank_str = "5.0 HP / 60 Gal Single-Stage"
        breaker_str = "240V 30A/40A Breaker (8/10 AWG)"
    elif req_comp_scfm <= 19.0:
        hp_tank_str = "5.0 HP / 60–80 Gal (IR SS5L5 / 2-Stage)"
        breaker_str = "240V 40A Breaker (8 AWG Copper)"
    else:
        hp_tank_str = "7.5 HP / 80 Gal Two-Stage (175 PSI)"
        breaker_str = "240V 50A + Mag Starter (6 AWG)"

    if req_comp_scfm >= 10.0 or float(pipe_ft) >= 60:
        pipe_spec = "3/4\" RapidAir Maxline (<1.1 PSI Drop)"
    else:
        pipe_spec = "1/2\" Line + 3/8\" Rubber Hose Reel"

    if dry_mode == "paint":
        dryer_spec = "3-Stage Coalescing + Desiccant Dryer"
    else:
        dryer_spec = "5µm Water Trap + High-Flow V-Couplers"

    # Reserve drawdown seconds from full tank (stage_psi down to 90 PSI) before pump even kicks on
    tank_gal = 80 if req_comp_scfm > 18 else (60 if req_comp_scfm > 9 else 20)
    tank_cuft = tank_gal / 7.48
    reserve_scfm_cuft = tank_cuft * ((float(stage_psi) - 90.0) / 14.7)
    buffer_secs = int(max(15, round((reserve_scfm_cuft / max(2.0, float(tool_scfm))) * 60.0)))

    return req_comp_scfm, hp_tank_str, breaker_str, pipe_spec, dryer_spec, buffer_secs

def generate_faq_data(preset_name, tool_scfm, duty_pct, stage_psi, pipe_ft, dry_mode):
    req_scfm, hp_tank, brk_str, pipe_s, dryer_s, buf_s = compute_air_specs(
        tool_scfm, duty_pct, stage_psi, pipe_ft, dry_mode
    )
    return [
        {
            "q": f"What size air compressor (SCFM, HP & Gallons) do I need for {preset_name} ({tool_scfm} SCFM @ 90 PSI)?",
            "a": f"Factoring in your tool's {tool_scfm} SCFM @ 90 PSI consumption at a {duty_pct}% duty cycle plus a 25% thermal safety buffer so the pump doesn't run 100% non-stop, you need a compressor rated for at least {req_scfm} SCFM @ 90 PSI—which corresponds to a {hp_tank}."
        },
        {
            "q": f"What size 240V circuit breaker and wire gauge is required for a {hp_tank} compressor?",
            "a": f"To handle motor startup inrush current without nuisance tripping, wire a dedicated {brk_str}. Note that true 5.0 HP and 7.5 HP 230V compressors require a magnetic motor starter box."
        },
        {
            "q": f"What diameter shop air piping and hose should I run for {pipe_ft} feet at {req_scfm} SCFM?",
            "a": f"For a {pipe_ft}-foot run at {req_scfm} SCFM, install {pipe_s} connected to the compressor tank via a 24-inch braided stainless vibration jumper hose, and use Milton High-Flow V-Style quick couplers."
        },
        {
            "q": "How do I stop water and oil droplets from ruining my HVLP paint job or plasma cutter?",
            "a": f"Hot air leaving a compressor pump is saturated with water vapor. Mount your wall filter at least 15–25 feet downstream of the tank (so the air cools and condenses in the 3/4\" Maxline pipe), and pass the air through a {dryer_s}."
        },
        {
            "q": "Why does a 175 PSI Two-Stage compressor give me more tool runtime than a 135 PSI Single-Stage?",
            "a": f"Your air tools only need 90 PSI at the regulator. A 135 PSI tank only has 45 PSI of reserve cushion above 90 PSI, whereas a 175 PSI Two-Stage tank has 85 PSI of reserve cushion—giving you ~{buf_s} seconds of pure tank buffer before the motor even turns on."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-blue-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['scfm_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['power_req']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-blue-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-blue-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top 60/80-Gal Air Compressors, Ultra-Quiet Units, HVLP Guns & Piping Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 CAGI SCFM @ 90 PSI & ASME Tank Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Shop Air Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">SCFM @ 90 PSI</th>
                        <th class="p-3.5">Electrical / Spec</th>
                        <th class="p-3.5">Key Shop Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-blue-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">SCFM / Output:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Motor / System:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Build / Pump:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Tank / Details:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Pneumatic Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Ingersoll+Rand+DEWALT+California+Air+Tools+Compressor+Maxline+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Shop Air Deals</span>
            <span>Save up to 30% on 60/80-Gal Cast-Iron Compressors, Ultra-Quiet 70 dBA Units, 3M HVLP Guns & Maxline Piping on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Air Compressor Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-blue-700 flex items-center justify-center text-white font-black text-lg shadow-sm">A</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Compressor SCFM, Tank Gallon & Piping Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-blue-800 transition">SCFM & Tank Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-blue-800 transition">Search Air Tools</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-blue-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">🔧 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-blue-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-blue-700 hover:bg-blue-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. SCFM & Tank Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-blue-800 hover:underline">🏠 Home — Master Air Compressor SCFM & Tank Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all air compressor SCFM calculators, tank gallon sizing guides, HVLP paint gun calculators, and daily pneumatic tool reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive air compressor SCFM calculator, tank gallon sizing guide, shop air piping calculator, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    req_scfm, hp_tank, _, _, _, _ = compute_air_specs(
        page_data["tool_scfm"], page_data["duty_pct"], page_data["stage_psi"],
        page_data["pipe_ft"], page_data["dry_mode"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {req_scfm} SCFM & Tank Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["tool_scfm"], page_data["duty_pct"],
        page_data["stage_psi"], page_data["pipe_ft"], page_data["dry_mode"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_scfm, _, _, _, _, _ = compute_air_specs(
            p["tool_scfm"], p["duty_pct"], p["stage_psi"], p["pipe_ft"], p["dry_mode"]
        )
        active_cls = "bg-blue-100 border-blue-700 text-blue-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-blue-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-blue-900 font-mono shrink-0">{p_scfm} SCFM</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Ingersoll+Rand+60+Gallon+Air+Compressor+RapidAir+Maxline+and+Desiccant+Dryer")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-blue-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🔧 CAGI SCFM @ 90 PSI, Tank Gallon Reserve, HVLP/Sandblast & Piping Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Air Compressor SCFM @ 90 PSI, Tank Gallon & Shop Piping Calculator" if is_home else f"{page_data['name']} — SCFM & Tank Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Air Tool SCFM, Duty Cycle & Piping Length</h2>
                        <p class="text-xs text-gray-600">Calculates required pump SCFM, HP/tank size, 240V breaker & shop air line diameter</p>
                    </div>
                    <span class="text-xs font-mono bg-blue-100 text-blue-900 border border-blue-300 px-2.5 py-1 rounded font-semibold">Live CAGI Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Pneumatic Tool or Shop Application Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <option value="{page_data['tool_scfm']},{page_data['duty_pct']},{page_data['stage_psi']},{page_data['pipe_ft']},{page_data['dry_mode']}">Current: {page_data['name']}</option>
                        <option value="13.0,85,135,75,paint">HVLP Automotive Paint Spray Gun (13.0 SCFM — 5HP 60-Gal + 3-Stage Dryer)</option>
                        <option value="18.0,90,175,50,paint">Sandblaster & Media Cabinet (#3/#4 Nozzle = 18.0 SCFM — 80-Gal Two-Stage)</option>
                        <option value="15.0,75,135,50,std">6\" Pneumatic DA Orbital Sander / Die Grinder (15.0 SCFM Continuous)</option>
                        <option value="6.0,35,135,50,std">1/2\" Titanium Air Impact Wrench & Ratchet (6.0 SCFM Intermittent)</option>
                        <option value="5.5,65,125,50,paint">50A–60A Pilot-Arc Plasma Cutter Air Supply (5.5 SCFM + Desiccant Dryer)</option>
                        <option value="4.2,40,125,50,std">120V Ultra-Quiet Woodshop Nailer & Blow Gun (4.2 SCFM @ 70 dBA)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="scfmInput" class="block text-sm font-bold text-gray-800 mb-1">Tool Air Consumption (SCFM @ 90 PSI)</label>
                        <input type="number" id="scfmInput" value="{page_data['tool_scfm']}" min="1.5" max="45.0" step="0.5" oninput="calculateAir()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Impact: 6 | HVLP Gun: 13 | DA Sander: 15 | Blaster: 18+</span>
                    </div>

                    <div>
                        <label for="dutyInput" class="block text-sm font-bold text-gray-800 mb-1">Tool Run Duty Cycle (%)</label>
                        <select id="dutyInput" onchange="calculateAir()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="35" {"selected" if page_data['duty_pct'] <= 40 else ""}>35% — Intermittent (Impact Guns, Nailers, Tire Inflation)</option>
                            <option value="65" {"selected" if 40 < page_data['duty_pct'] <= 70 else ""}>65% — Moderate Continuous (Plasma Cutting, Die Grinding)</option>
                            <option value="80" {"selected" if 70 < page_data['duty_pct'] <= 85 else ""}>80% — Heavy Continuous (HVLP Car Painting, DA Sanding)</option>
                            <option value="95" {"selected" if page_data['duty_pct'] > 85 else ""}>95% — Non-Stop Industrial (Cabinet Sandblasting, 2 Techs)</option>
                        </select>
                    </div>

                    <div>
                        <label for="stageInput" class="block text-sm font-bold text-gray-800 mb-1">Compressor Stage & Max Tank PSI</label>
                        <select id="stageInput" onchange="calculateAir()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="125" {"selected" if page_data['stage_psi'] == "125" else ""}>125 PSI Max — Portable / Ultra-Quiet 120V</option>
                            <option value="135" {"selected" if page_data['stage_psi'] in ("135", "155") else ""}>135–155 PSI Max — Single-Stage 240V Stationary</option>
                            <option value="175" {"selected" if page_data['stage_psi'] == "175" else ""}>175 PSI Max — Two-Stage Commercial (Max Reserve!)</option>
                        </select>
                    </div>

                    <div>
                        <label for="pipeFtInput" class="block text-sm font-bold text-gray-800 mb-1">Shop Air Line Run Length (Feet)</label>
                        <input type="number" id="pipeFtInput" value="{page_data['pipe_ft']}" min="15" max="300" step="15" oninput="calculateAir()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-blue-700">
                        <span class="text-[11px] text-gray-600">Sizes 1/2\" vs 3/4\" RapidAir Maxline wall piping</span>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="dryInput" class="block text-sm font-bold text-gray-800 mb-1">Air Moisture & Oil Filtration Requirement</label>
                        <select id="dryInput" onchange="calculateAir()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="std" {"selected" if page_data['dry_mode'] == "std" else ""}>Standard Mechanic / Woodshop (5-Micron Water Trap + High-Flow V-Couplers)</option>
                            <option value="paint" {"selected" if page_data['dry_mode'] == "paint" else ""}>HVLP Auto Painting / Plasma / Blasting (3-Stage Coalescing + Desiccant Dryer)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">2. Engineered Compressor & Piping Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Shop Air System</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-blue-100 border border-blue-300 rounded-xl p-3.5">
                        <span class="text-xs text-blue-950 font-semibold block">Min. Compressor SCFM</span>
                        <span id="resReqSCFM" class="text-2xl font-black text-blue-800">13.8 SCFM</span>
                        <span id="resReserve" class="text-[11px] text-blue-900 block mt-0.5">@ 90 PSI (+25% Buffer)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Recommended HP & Tank</span>
                        <span id="resHpTank" class="text-base font-black text-gray-900">5 HP / 60 Gal</span>
                        <span id="resBreaker" class="text-[11px] text-emerald-800 font-bold block mt-0.5">240V 30A/40A (8 AWG)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Shop Air Piping Spec</span>
                        <span id="resPipeSpec" class="text-sm font-extrabold text-gray-900">3/4\" Maxline Kit</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">+ 24\" Stainless Whip</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Air Dryer & Couplers</span>
                        <span id="resDryerSpec" class="text-sm font-extrabold text-amber-800">3-Stage Desiccant</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">+ Milton V-Style Plugs</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-blue-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recAirTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Compressor & Piping Match...</h3>
                    <p id="recAirDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Air Compressor &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Piping, Dryer & Tools
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Air Compressors, HVLP Paint Guns, Impact Wrenches & Maxline Piping</h2>
                <p class="text-sm text-gray-700">Search any brand (Ingersoll Rand, California Air Tools, DeWalt, 3M Performance, RapidAir Maxline, DeVilbiss, BluBird, Milton) on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Ingersoll Rand 60 Gallon Compressor, California Air Tools 10020C, RapidAir Maxline 3/4..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-700" required>
                    <button type="submit" class="bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Ingersoll Rand SS5L5 60 Gallon Air Compressor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Ingersoll Rand 60-Gal</a>
                    <a href="{amz_url('California Air Tools Ultra Quiet Air Compressor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">California Air 70 dBA</a>
                    <a href="{amz_url('RapidAir Maxline M7500 3/4 Inch Air Piping Kit')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">Maxline 3/4\" Shop Piping</a>
                    <a href="{amz_url('3M Performance HVLP Spray Gun Kit')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">3M HVLP Spray Guns</a>
                    <a href="{amz_url('3 Stage Desiccant Air Dryer Filter Regulator')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-blue-200 text-gray-800 border border-gray-300 rounded-full transition">3-Stage Desiccant Dryers</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Verified Shop Pneumatic Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Air Compressors, HVLP Guns, Impact Wrenches & Piping Kits</h2>
                </div>
                <a href="{amz_url('Best Selling Air Compressors and Pneumatic Tools')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-blue-800 hover:text-blue-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Air Compressor, HVLP Gun & Pneumatic Tool Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-blue-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-700 text-white px-2.5 py-1 rounded">Complete Zero-Moisture Garage Air Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Plumbing a 60-Gallon or 80-Gallon Compressor for Auto Painting & Fab?</h2>
                <p class="text-sm text-gray-800">Eliminate pressure drop and water fisheyes by pairing a 5 HP Cast-Iron Compressor with a 24\" Stainless Vibration Jumper Hose, 100-Ft 3/4\" RapidAir Maxline Piping Kit, and 3-Stage Desiccant Air Dryer.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Compressor + Maxline + Dryer Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Air Tool SCFM, Sandblaster & Shop Piping Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact pneumatic tool or SCFM tier below for pre-calculated compressor horsepower, tank gallons, and 240V breaker sizes.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-800">SCFM vs CFM, Two-Stage & Moisture Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-blue-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-blue-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-blue-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-blue-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("scfmInput").value = parts[0];
                document.getElementById("dutyInput").value = parts[1];
                document.getElementById("stageInput").value = parts[2];
                document.getElementById("pipeFtInput").value = parts[3];
                document.getElementById("dryInput").value = parts[4];
                calculateAir();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateAir() {{
            const toolSCFM = parseFloat(document.getElementById("scfmInput").value) || 13.0;
            const dutyPct = parseFloat(document.getElementById("dutyInput").value) || 85;
            const stagePsi = parseFloat(document.getElementById("stageInput").value) || 135;
            const pipeFt = parseFloat(document.getElementById("pipeFtInput").value) || 75;
            const dryMode = document.getElementById("dryInput").value || "paint";

            const effSCFM = toolSCFM * (dutyPct / 100.0) * 1.25;
            const reqSCFM = Math.max(toolSCFM * 0.85, effSCFM).toFixed(1);

            let hpTank = "5.0 HP / 60 Gal";
            let brkStr = "240V 30A/40A (8 AWG)";
            if (reqSCFM <= 5.5) {{
                hpTank = "2.0 HP / 10–20 Gal (120V)";
                brkStr = "120V 15A/20A (12 AWG)";
            }} else if (reqSCFM <= 10.5) {{
                hpTank = "3.0–3.7 HP / 30–60 Gal";
                brkStr = "240V 20A/30A (10 AWG)";
            }} else if (reqSCFM <= 16.0) {{
                hpTank = "5.0 HP / 60 Gal Cast-Iron";
                brkStr = "240V 30A/40A (8/10 AWG)";
            }} else if (reqSCFM <= 19.0) {{
                hpTank = "5.0 HP / 60–80 Gal (IR SS5L5)";
                brkStr = "240V 40A (8 AWG Copper)";
            }} else {{
                hpTank = "7.5 HP / 80 Gal Two-Stage";
                brkStr = "240V 50A + Mag Starter (6 AWG)";
            }}

            const pipeSpec = (reqSCFM >= 10.0 || pipeFt >= 60) ? "3/4\\\" RapidAir Maxline" : "1/2\\\" Line + 3/8\\\" Reel";
            const dryerSpec = dryMode === "paint" ? "3-Stage Desiccant Dryer" : "5µm Trap + V-Couplers";

            const tankGal = reqSCFM > 18 ? 80 : (reqSCFM > 9 ? 60 : 20);
            const reserveCuFt = (tankGal / 7.48) * ((stagePsi - 90.0) / 14.7);
            const bufSecs = Math.max(15, Math.round((reserveCuFt / Math.max(2, toolSCFM)) * 60));

            document.getElementById("resReqSCFM").textContent = reqSCFM + " SCFM";
            document.getElementById("resReserve").textContent = "~" + bufSecs + "s Tank Buffer (@ " + stagePsi + " PSI)";
            document.getElementById("resHpTank").textContent = hpTank;
            document.getElementById("resBreaker").textContent = brkStr;
            document.getElementById("resPipeSpec").textContent = pipeSpec;
            document.getElementById("resDryerSpec").textContent = dryerSpec;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "RapidAir Maxline M7500 3/4 Piping Kit and 3 Stage Desiccant Air Dryer";

            if (reqSCFM <= 6.0) {{
                recTitle = "California Air Tools 10020C / 20020D 2.0 HP Ultra-Quiet (70 dBA) Compressor";
                recDesc = "Whisper-quiet 120V oil-free air matched to " + reqSCFM + " SCFM @ 90 PSI tools.";
                primaryQuery = "California Air Tools 10020C 2.0 HP Ultra Quiet Air Compressor";
                secondaryQuery = "BluBird 3/8 50 Ft Retractable Rubber Air Hose Reel and Milton V Couplers";
            }} else if (reqSCFM <= 18.5) {{
                recTitle = "Ingersoll Rand SS5L5 (18.1 SCFM) or DEWALT 60-Gallon 240V Cast-Iron Compressor";
                recDesc = "America's #1 60-gallon shop setup delivering continuous air for HVLP guns, DA sanders, and impacts.";
                primaryQuery = "Ingersoll Rand SS5L5 DEWALT 60 Gallon Stationary Air Compressor";
            }} else {{
                recTitle = "Ingersoll Rand / Quincy 5 HP – 7.5 HP 80-Gallon Two-Stage (175 PSI) Compressor";
                recDesc = "Heavy commercial two-stage cast-iron pump built for continuous sandblasting and multi-tech shops.";
                primaryQuery = "Ingersoll Rand Quincy 80 Gallon Two Stage Air Compressor 230V";
            }}

            document.getElementById("recAirTitle").textContent = recTitle;
            document.getElementById("recAirDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateAir);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-blue-700 transition block">
            <span class="text-[11px] font-bold text-blue-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & SCFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-blue-800">Daily Shop Air Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Shop Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">SCFM / Output</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Motor / System</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Build / Pump</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Tank / Details</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Tool SCFM & Tank Size
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On 90-PSI Flow Rate, Duty Cycle & Moisture Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-blue-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our pneumatic shop benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Compressor & Pneumatic Tool Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-blue-800">Home & SCFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-blue-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-blue-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-blue-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "HVLP Automotive Paint Spray Gun & DA Sander (13.0 SCFM @ 90 PSI)",
        "tool_scfm": 13.0,
        "duty_pct": 85,
        "stage_psi": "135",
        "pipe_ft": 75,
        "dry_mode": "paint",
        "desc": "Calculate exact air compressor SCFM @ 90 PSI, tank gallon capacity (20/30/60/80 gal), HVLP & sandblaster air demand, 3/4\" shop air piping, and 240V breaker sizing—plus read 3 new pneumatic reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Air Compressor & SCFM Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
