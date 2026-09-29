import json
import uuid
import datetime

# New categories to add
new_categories = [
    {"id": "CAT-ENGINES", "name": "Internal Combustion Engines", "sector_id": "SEC-MECH"},
    {"id": "CAT-PRESSURE_VESSELS", "name": "Pressure Vessels", "sector_id": "SEC-MECH"},
    {"id": "CAT-COMPRESSORS", "name": "Compressors", "sector_id": "SEC-MECH"}
]

standards_to_add = [
    # ELECTRICAL
    {
        "standard_number": "IS 2026-1",
        "title": "Power Transformers - Part 1: General",
        "short_description": "General requirements for power transformers, including ratings, cooling methods, and performance.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-TRANSFORMERS",
        "scope_text": "Specifies general requirements for three-phase and single-phase power transformers.",
        "included_products": ["Power transformers", "Distribution transformers"],
        "excluded_products": ["Instrument transformers", "Traction transformers", "Starting transformers"],
        "applications": ["Power generation", "Power transmission", "Substations"]
    },
    {
        "standard_number": "IS 11171",
        "title": "Dry-Type Power Transformers",
        "short_description": "Specifies requirements for dry-type power transformers used in specific environments.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-TRANSFORMERS",
        "scope_text": "Applies to dry-type power transformers (including auto-transformers) having highest voltage for equipment up to and including 36 kV.",
        "included_products": ["Dry-type transformers", "Cast resin transformers"],
        "excluded_products": ["Oil-filled transformers"],
        "applications": ["Indoor substations", "Commercial buildings", "Industrial plants"]
    },
    {
        "standard_number": "IS 1651",
        "title": "Stationary Cells and Batteries, Lead-Acid Type (with Tubular Positive Plates)",
        "short_description": "Requirements and tests for stationary lead-acid batteries with tubular positive plates.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-ELECEQ",
        "scope_text": "Covers stationary lead-acid cells and batteries with tubular positive plates used for standby power.",
        "included_products": ["Lead-acid batteries", "Tubular batteries", "Stationary cells"],
        "excluded_products": ["Automotive batteries", "Traction batteries"],
        "applications": ["UPS systems", "Telecommunications", "Emergency lighting", "Switchgear operation"]
    },
    {
        "standard_number": "IS 1554-1",
        "title": "PVC Insulated (Heavy Duty) Electric Cables - Part 1: For Working Voltages up to and Including 1100 V",
        "short_description": "Requirements for PVC insulated heavy duty electrical cables for low voltage applications.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-CABLES",
        "scope_text": "Specifies requirements for PVC insulated, PVC sheathed heavy duty electric cables for working voltages up to and including 1100 V.",
        "included_products": ["PVC insulated cables", "Armoured cables", "Unarmoured cables", "Heavy duty cables"],
        "excluded_products": ["Flexible cables", "High voltage cables"],
        "applications": ["Power distribution", "Underground wiring", "Industrial wiring"]
    },
    {
        "standard_number": "IS 7098-1",
        "title": "Crosslinked Polyethylene Insulated PVC Sheathed Cables - Part 1: For Working Voltage up to and Including 1100 V",
        "short_description": "Requirements for XLPE insulated electrical cables for voltages up to 1.1 kV.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-CABLES",
        "scope_text": "Specifies requirements for XLPE insulated and PVC sheathed cables for power distribution up to 1100 V.",
        "included_products": ["XLPE cables", "Armoured XLPE cables", "Power cables"],
        "excluded_products": ["Elastomeric cables", "High voltage XLPE cables"],
        "applications": ["Industrial power distribution", "Underground mains", "Commercial power supply"]
    },
    {
        "standard_number": "IS 13947-2",
        "title": "Low-Voltage Switchgear and Controlgear - Part 2: Circuit Breakers",
        "short_description": "Specifies performance and testing requirements for low-voltage circuit breakers.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-ELECEQ",
        "scope_text": "Applies to circuit-breakers, the main contacts of which are intended to be connected to circuits, the rated voltage of which does not exceed 1000 V a.c. or 1500 V d.c.",
        "included_products": ["Circuit breakers", "MCCB", "ACB"],
        "excluded_products": ["Miniature circuit breakers (MCB for household use)"],
        "applications": ["Switchboards", "Motor control centers", "Industrial power control"]
    },
    {
        "standard_number": "IS 12615",
        "title": "Line Operated Three Phase a.c. Motors - Energy Efficiency Classes and Performance Specification",
        "short_description": "Specifies energy efficiency classes (IE codes) and performance for 3-phase induction motors.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-MOTORS",
        "scope_text": "Specifies the efficiency classes (IE2, IE3, IE4) and performance requirements for single-speed, three-phase, 50 Hz, cage induction motors.",
        "included_products": ["Energy efficient motors", "Three-phase induction motors", "Cage motors"],
        "excluded_products": ["Single-phase motors", "Variable speed drive motors"],
        "applications": ["Industrial drives", "Pumps", "Compressors", "Fans"]
    },
    {
        "standard_number": "IS 3043",
        "title": "Code of Practice for Earthing",
        "short_description": "Comprehensive guidelines for design, installation, and maintenance of earthing systems.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-ELECEQ",
        "scope_text": "Provides guidance on the methods that may be adopted to earth an electrical system for the purpose of limiting the potential (with respect to the general mass of earth) of current carrying conductors.",
        "included_products": ["Earthing electrodes", "Earthing conductors", "Earth pits"],
        "excluded_products": [],
        "applications": ["Building electrification", "Substations", "Industrial installations", "Lightning protection"]
    },
    {
        "standard_number": "IS 16444",
        "title": "A.C. Static Direct Connected Watt-hour Smart Meter Class 1 and 2 - Specification",
        "short_description": "Specifies requirements for smart electricity meters with bi-directional communication.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-ELECEQ",
        "scope_text": "Covers a.c. static direct connected watt-hour smart meters of class 1 and 2 for measurement of active energy.",
        "included_products": ["Smart meters", "Energy meters", "AMI meters"],
        "excluded_products": ["Transformer operated meters", "Prepayment meters"],
        "applications": ["Utility metering", "Smart grid", "Residential billing", "Commercial billing"]
    },

    # MECHANICAL
    {
        "standard_number": "IS 5120",
        "title": "Technical Requirements for Rotodynamic Special Purpose Pumps",
        "short_description": "General requirements for special purpose rotodynamic (centrifugal, mixed flow, and axial flow) pumps.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-PUMPS",
        "scope_text": "Covers the technical requirements for rotodynamic special purpose pumps used for handling liquids other than clear, cold water.",
        "included_products": ["Chemical pumps", "Slurry pumps", "Sewage pumps", "Special purpose pumps"],
        "excluded_products": ["Agricultural pumps", "Standard water pumps"],
        "applications": ["Chemical processing", "Effluent treatment", "Mining", "Industrial fluid handling"]
    },
    {
        "standard_number": "IS 1520",
        "title": "Horizontal Centrifugal Pumps for Clear, Cold and Fresh Water",
        "short_description": "Specifications for horizontal centrifugal pumps used for pumping clean water.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-PUMPS",
        "scope_text": "Covers horizontal centrifugal pumps for clear, cold and fresh water for agricultural and general purposes.",
        "included_products": ["Horizontal centrifugal pumps", "Water pumps"],
        "excluded_products": ["Submersible pumps", "Chemical pumps"],
        "applications": ["Irrigation", "Water supply", "General pumping"]
    },
    {
        "standard_number": "IS 6595",
        "title": "Centrifugal Pumps for Agricultural Applications",
        "short_description": "Requirements for centrifugal pumps specifically designed for agricultural use.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-PUMPS",
        "scope_text": "Specifies requirements for centrifugal pumps used primarily for agricultural purposes.",
        "included_products": ["Agricultural pumps", "Monoset pumps", "Centrifugal pumps"],
        "excluded_products": ["Industrial process pumps"],
        "applications": ["Farming", "Irrigation", "Rural water supply"]
    },
    {
        "standard_number": "IS 8034",
        "title": "Submersible Pumpsets for Clear, Cold, Fresh Water",
        "short_description": "Specifications for submersible pumpsets used in borewells for water extraction.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-PUMPS",
        "scope_text": "Covers submersible pumpsets suitable for installation in boreholes of nominal diameter 100 mm and above for clear, cold, fresh water.",
        "included_products": ["Submersible pumps", "Borewell pumps", "Submersible motors"],
        "excluded_products": ["Open well submersibles", "Sewage submersibles"],
        "applications": ["Groundwater extraction", "Municipal water supply", "Irrigation"]
    },
    {
        "standard_number": "IS 325",
        "title": "Three-Phase Induction Motors",
        "short_description": "General requirements for three-phase induction motors.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-MOTORS",
        "scope_text": "Covers three-phase induction motors for general purpose applications.",
        "included_products": ["Induction motors", "Squirrel cage motors", "Slip ring motors"],
        "excluded_products": ["Single-phase motors", "Special purpose motors"],
        "applications": ["Industrial drives", "Machinery", "Pumps", "General engineering"]
    },
    {
        "standard_number": "IS 10000-1",
        "title": "Methods of Tests for Internal Combustion Engines - Part 1: Glossary of Terms",
        "short_description": "Terminology and general definitions for internal combustion engines.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-ENGINES",
        "scope_text": "Covers the glossary of terms applicable to internal combustion engines.",
        "included_products": ["Internal combustion engines", "Diesel engines", "Petrol engines"],
        "excluded_products": ["Gas turbines", "Steam engines"],
        "applications": ["Generators", "Automotive", "Industrial power", "Marine"]
    },
    {
        "standard_number": "IS 4111-1",
        "title": "Code of Practice for Ancillary Structures in Sewerage System - Part 1: Manholes",
        "short_description": "Design and construction guidelines for manholes in sewerage systems.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-VALVES",
        "scope_text": "Covers the requirements for design, construction, and safety of manholes in sewerage systems.",
        "included_products": ["Manholes", "Sewerage structures", "Manhole covers"],
        "excluded_products": ["Pipes", "Pumping stations"],
        "applications": ["Municipal sewerage", "Drainage networks", "Urban infrastructure"]
    },
    {
        "standard_number": "IS 2825",
        "title": "Code for Unfired Pressure Vessels",
        "short_description": "Comprehensive code for the design, construction, inspection and testing of unfired pressure vessels.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-PRESSURE_VESSELS",
        "scope_text": "Covers the design, fabrication, inspection, testing, and certification of unfired pressure vessels.",
        "included_products": ["Pressure vessels", "Storage tanks", "Heat exchangers (shell)"],
        "excluded_products": ["Fired boilers", "Nuclear vessels", "Gas cylinders"],
        "applications": ["Chemical plants", "Petrochemical", "Oil and gas", "Process industries"]
    },
    {
        "standard_number": "IS 6206",
        "title": "Guide for Selection, Installation and Maintenance of Air Compressors",
        "short_description": "Guidelines for proper selection, setup, and upkeep of industrial air compressors.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-COMPRESSORS",
        "scope_text": "Provides guidance on the selection, installation, and maintenance of various types of air compressors.",
        "included_products": ["Air compressors", "Reciprocating compressors", "Rotary compressors"],
        "excluded_products": ["Gas compressors", "Refrigerant compressors"],
        "applications": ["Pneumatic systems", "Industrial air supply", "Manufacturing plants"]
    },

    # WATER / SANITATION
    {
        "standard_number": "IS 4985",
        "title": "Unplasticized PVC Pipes for Potable Water Supplies",
        "short_description": "Specifications for UPVC pipes used for drinking water supply systems.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-PIPES",
        "scope_text": "Covers requirements for unplasticized polyvinyl chloride (UPVC) pipes intended for potable water supplies.",
        "included_products": ["UPVC pipes", "PVC pipes", "Water pipes"],
        "excluded_products": ["CPVC pipes", "Sewer pipes"],
        "applications": ["Potable water supply", "Plumbing", "Agricultural piping"]
    },
    {
        "standard_number": "IS 15778",
        "title": "Chlorinated Polyvinyl Chloride (CPVC) Pipes for Potable Hot and Cold Water Distribution Supplies",
        "short_description": "Requirements for CPVC pipes suitable for conveying hot and cold potable water.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-PIPES",
        "scope_text": "Specifies requirements for CPVC pipes for hot and cold water distribution systems.",
        "included_products": ["CPVC pipes", "Hot water pipes"],
        "excluded_products": ["UPVC pipes", "Industrial chemical pipes"],
        "applications": ["Indoor plumbing", "Hot water distribution", "Residential water systems"]
    },
    {
        "standard_number": "IS 778",
        "title": "Copper Alloy Gate, Globe and Check Valves for Water Works Purposes",
        "short_description": "Specifications for bronze and brass valves used in water plumbing.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-VALVES",
        "scope_text": "Covers copper alloy gate, globe and check valves of nominal sizes from 8 mm to 100 mm for water works.",
        "included_products": ["Gate valves", "Globe valves", "Check valves", "Brass valves", "Bronze valves"],
        "excluded_products": ["Cast iron valves", "Butterfly valves"],
        "applications": ["Building plumbing", "Water distribution", "Residential water works"]
    },
    {
        "standard_number": "IS 14846",
        "title": "Sluice Valves for Water Works Purposes (50 mm to 1200 mm Size)",
        "short_description": "Requirements for cast iron sluice (gate) valves for large water works.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-VALVES",
        "scope_text": "Covers requirements for flanged and socket-ended sluice valves used for water works.",
        "included_products": ["Sluice valves", "Cast iron gate valves", "Large valves"],
        "excluded_products": ["Small copper alloy valves"],
        "applications": ["Municipal water supply", "Water treatment plants", "Main distribution networks"]
    },
    {
        "standard_number": "IS 13095",
        "title": "Butterfly Valves for General Purposes",
        "short_description": "Specifications for butterfly valves used for flow control in pipelines.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-VALVES",
        "scope_text": "Covers butterfly valves for general purposes for nominal sizes 40 mm to 2000 mm.",
        "included_products": ["Butterfly valves", "Wafer valves", "Flanged butterfly valves"],
        "excluded_products": ["Sluice valves", "Check valves"],
        "applications": ["Water treatment", "HVAC cooling water", "Industrial fluid control"]
    },
    {
        "standard_number": "IS 2556-1",
        "title": "Vitreous Sanitary Appliances (Vitreous China) - Part 1: General Requirements",
        "short_description": "General material and testing requirements for vitreous china sanitaryware.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-SANITARY",
        "scope_text": "Covers general requirements for material, manufacture, methods of test and inspection of vitreous sanitary appliances.",
        "included_products": ["Wash basins", "Water closets", "Urinals", "Vitreous china products"],
        "excluded_products": ["Stainless steel sinks", "Plastic sanitaryware"],
        "applications": ["Bathrooms", "Public toilets", "Residential sanitation", "Commercial restrooms"]
    },
    {
        "standard_number": "IS 774",
        "title": "Flushing Cisterns for Water Closets and Urinals (Other Than Plastic Cisterns)",
        "short_description": "Requirements for cast iron, vitreous china, and other non-plastic flushing cisterns.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-SANITARY",
        "scope_text": "Covers flushing cisterns (manually operated) for water closets and urinals, excluding plastic cisterns.",
        "included_products": ["Flushing cisterns", "Flush tanks", "Vitreous china cisterns"],
        "excluded_products": ["Plastic cisterns", "Flush valves"],
        "applications": ["Sanitary installations", "Bathrooms", "Toilets"]
    },

    # SAFETY / FIRE
    {
        "standard_number": "IS 15683",
        "title": "Portable Fire Extinguishers - Performance and Construction",
        "short_description": "Comprehensive standard for design, construction, and performance of all portable fire extinguishers.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-FIRE",
        "scope_text": "Specifies requirements for portable fire extinguishers, including water, foam, powder, and carbon dioxide types.",
        "included_products": ["Portable fire extinguishers", "DCP extinguishers", "CO2 extinguishers", "Foam extinguishers"],
        "excluded_products": ["Wheeled fire extinguishers", "Fixed fire fighting systems"],
        "applications": ["Fire safety in buildings", "Industrial fire protection", "Commercial spaces"]
    },
    {
        "standard_number": "IS 2189",
        "title": "Selection, Installation and Maintenance of Automatic Fire Detection and Alarm System",
        "short_description": "Code of practice for setting up fire detection and alarm networks.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-FIRE",
        "scope_text": "Covers the planning, design, selection, installation, and maintenance of fire detection and alarm systems.",
        "included_products": ["Fire alarm panels", "Smoke detectors", "Heat detectors", "Manual call points"],
        "excluded_products": ["Fire suppression systems", "Sprinklers"],
        "applications": ["Building safety", "Industrial facilities", "Commercial complexes", "Hospitals"]
    },
    {
        "standard_number": "IS 2190",
        "title": "Selection, Installation and Maintenance of First-Aid Fire Extinguishers - Code of Practice",
        "short_description": "Guidelines on how to select and place the right fire extinguishers for different fire risks.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-FIRE",
        "scope_text": "Provides recommendations for the selection, installation, maintenance and testing of first-aid fire extinguishers.",
        "included_products": ["Fire extinguisher selection", "Fire extinguisher maintenance"],
        "excluded_products": ["Fire extinguisher manufacturing (see IS 15683)"],
        "applications": ["Facility management", "Fire safety compliance", "Workplace safety"]
    },
    {
        "standard_number": "IS 2925",
        "title": "Industrial Safety Helmets",
        "short_description": "Requirements for safety helmets to protect against falling objects in workplaces.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Specifies requirements regarding material, construction, workmanship, and performance of industrial safety helmets.",
        "included_products": ["Safety helmets", "Hard hats", "Protective headgear"],
        "excluded_products": ["Firefighter helmets", "Motorcycle helmets", "Riot helmets"],
        "applications": ["Construction sites", "Manufacturing plants", "Mining", "Heavy industry"]
    },
    {
        "standard_number": "IS 15298-2",
        "title": "Personal Protective Equipment - Safety Footwear",
        "short_description": "Specifications for safety shoes and boots with protective toe caps.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Specifies basic and additional (optional) requirements for safety footwear used for general purpose.",
        "included_products": ["Safety shoes", "Safety boots", "Protective footwear"],
        "excluded_products": ["Occupational footwear (without toe caps)"],
        "applications": ["Industrial safety", "Construction", "Logistics", "Workplace PPE"]
    },
    {
        "standard_number": "IS 3521-1",
        "title": "Personal Fall Arrest Systems - Part 1: Full Body Harnesses",
        "short_description": "Requirements for full body harnesses used for working at heights.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Specifies requirements, test methods, marking and information supplied by the manufacturer for full body harnesses.",
        "included_products": ["Full body harnesses", "Fall protection harnesses", "Safety belts"],
        "excluded_products": ["Lanyards", "Energy absorbers", "Work positioning belts"],
        "applications": ["Working at heights", "Construction scaffolding", "Telecom towers", "Maintenance"]
    },
    {
        "standard_number": "IS 4770",
        "title": "Rubber Gloves for Electrical Purposes",
        "short_description": "Specifications for insulating rubber gloves used by electrical workers.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Covers requirements for insulating rubber gloves used for protection of electrical workers from electrical shock.",
        "included_products": ["Electrical safety gloves", "Insulating gloves", "Rubber gloves"],
        "excluded_products": ["Medical gloves", "Chemical resistant gloves"],
        "applications": ["Electrical maintenance", "Live line working", "Substation operation"]
    },

    # HVAC
    {
        "standard_number": "IS 1391-1",
        "title": "Room Air Conditioners - Part 1: Unitary Air Conditioners",
        "short_description": "Specifications for unitary (window-type) room air conditioners.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-HVAC",
        "scope_text": "Covers unitary room air conditioners intended for window or through-the-wall installation.",
        "included_products": ["Window air conditioners", "Unitary ACs"],
        "excluded_products": ["Split ACs", "Packaged ACs"],
        "applications": ["Residential cooling", "Small offices", "Individual rooms"]
    },
    {
        "standard_number": "IS 1391-2",
        "title": "Room Air Conditioners - Part 2: Split Air Conditioners",
        "short_description": "Specifications and testing methods for split-type room air conditioners.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-HVAC",
        "scope_text": "Specifies the requirements and test methods for split room air conditioners.",
        "included_products": ["Split air conditioners", "Wall mounted ACs", "Ductless splits"],
        "excluded_products": ["Window ACs", "VRF systems", "Chillers"],
        "applications": ["Residential air conditioning", "Commercial spaces", "Offices"]
    },
    {
        "standard_number": "IS 8148",
        "title": "Packaged Air Conditioners",
        "short_description": "Requirements for packaged air conditioning units for larger spaces.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-HVAC",
        "scope_text": "Covers packaged air conditioners (including ductable units) for commercial and industrial applications.",
        "included_products": ["Packaged ACs", "Ductable ACs", "Floor standing ACs"],
        "excluded_products": ["Room ACs", "Central chiller plants"],
        "applications": ["Server rooms", "Commercial buildings", "Retail stores", "Auditoriums"]
    },
    {
        "standard_number": "IS 659",
        "title": "Safety Code for Air Conditioning",
        "short_description": "Safety guidelines for the design and installation of air conditioning systems.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-HVAC",
        "scope_text": "Lays down safety practices for the design, installation, operation, and maintenance of air conditioning systems.",
        "included_products": ["Air conditioning systems", "Ductwork systems"],
        "excluded_products": ["Cold storages"],
        "applications": ["Central air conditioning", "HVAC design", "Building safety"]
    },
    {
        "standard_number": "IS 660",
        "title": "Safety Code for Mechanical Refrigeration",
        "short_description": "Safety guidelines for refrigeration plants and cold storages.",
        "status": "CURRENT",
        "sector_id": "SEC-MECH",
        "category_id": "CAT-HVAC",
        "scope_text": "Covers safety requirements in the design, construction, installation, operation, and inspection of mechanical refrigeration systems.",
        "included_products": ["Refrigeration plants", "Cold storages", "Ammonia plants", "Freon systems"],
        "excluded_products": ["Household refrigerators"],
        "applications": ["Food processing", "Cold chain", "Industrial refrigeration", "Ice plants"]
    },

    # LIGHTING
    {
        "standard_number": "IS 16101",
        "title": "General Lighting - LEDs and LED Modules - Terms and Definitions",
        "short_description": "Standardized terminology for LED lighting products.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-LIGHTING",
        "scope_text": "Provides terms and definitions for LEDs, LED modules, and related equipment for general lighting.",
        "included_products": ["LED lighting vocabulary"],
        "excluded_products": ["Performance requirements (see specific standards)"],
        "applications": ["Lighting specifications", "Procurement documentation", "Technical literature"]
    },
    {
        "standard_number": "IS 16102-1",
        "title": "Self-Ballasted LED Lamps for General Lighting Services - Part 1: Safety Requirements",
        "short_description": "Safety specifications for common LED bulbs (self-ballasted).",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-LIGHTING",
        "scope_text": "Specifies safety and interchangeability requirements for self-ballasted LED lamps for general lighting.",
        "included_products": ["LED bulbs", "Self-ballasted LED lamps"],
        "excluded_products": ["LED tubes", "Luminaires"],
        "applications": ["Domestic lighting", "Commercial lighting", "General illumination"]
    },
    {
        "standard_number": "IS 10322-1",
        "title": "Luminaires - Part 1: General Requirements and Tests",
        "short_description": "General safety and testing requirements for all types of light fixtures.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-LIGHTING",
        "scope_text": "Covers general requirements for classification, marking, mechanical construction, and electrical safety of luminaires.",
        "included_products": ["Luminaires", "Light fixtures", "Lighting enclosures"],
        "excluded_products": ["Lamps (bulbs/tubes) themselves"],
        "applications": ["Lighting manufacturing", "Fixture selection", "Safety testing"]
    },
    {
        "standard_number": "IS 10322-5-1",
        "title": "Luminaires - Part 5: Particular Requirements - Sec 1: Fixed General Purpose Luminaires",
        "short_description": "Specific requirements for fixed (ceiling/wall mounted) light fixtures.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-LIGHTING",
        "scope_text": "Specifies requirements for fixed general purpose luminaires for use with tungsten filament, tubular fluorescent and other discharge lamps.",
        "included_products": ["Fixed luminaires", "Ceiling lights", "Wall lights", "Panel lights"],
        "excluded_products": ["Portable luminaires", "Street lighting", "Floodlights"],
        "applications": ["Indoor lighting", "Office lighting", "Architectural lighting"]
    },

    # CIVIL
    {
        "standard_number": "IS 456",
        "title": "Plain and Reinforced Concrete - Code of Practice",
        "short_description": "The fundamental code for design and construction of concrete structures in India.",
        "status": "CURRENT",
        "sector_id": "SEC-CIVIL",
        "category_id": "CAT-CONCRETE",
        "scope_text": "Deals with the general structural use of plain and reinforced concrete.",
        "included_products": ["Plain concrete", "Reinforced concrete", "Concrete mix design"],
        "excluded_products": ["Prestressed concrete"],
        "applications": ["Building construction", "Structural engineering", "Infrastructure projects"]
    },
    {
        "standard_number": "IS 383",
        "title": "Coarse and Fine Aggregate for Concrete",
        "short_description": "Specifications for sand, gravel, and crushed stone used in concrete mixtures.",
        "status": "CURRENT",
        "sector_id": "SEC-CIVIL",
        "category_id": "CAT-CONCRETE",
        "scope_text": "Covers the requirements for naturally occurring and manufactured aggregates for use in concrete.",
        "included_products": ["Coarse aggregates", "Fine aggregates", "Sand", "Crushed stone", "M-sand"],
        "excluded_products": ["Lightweight aggregates", "Heavyweight aggregates"],
        "applications": ["Concrete production", "Construction materials procurement", "Ready-mix concrete"]
    },
    {
        "standard_number": "IS 1786",
        "title": "High Strength Deformed Steel Bars and Wires for Concrete Reinforcement",
        "short_description": "Specifications for TMT and other high-strength rebars used in reinforced concrete.",
        "status": "CURRENT",
        "sector_id": "SEC-CIVIL",
        "category_id": "CAT-STEEL",
        "scope_text": "Specifies requirements for high strength deformed steel bars and wires for concrete reinforcement.",
        "included_products": ["TMT bars", "Deformed steel bars", "Reinforcement steel", "Rebars"],
        "excluded_products": ["Mild steel bars", "Structural steel sections"],
        "applications": ["Reinforced concrete structures", "Building foundations", "Slabs and columns"]
    },
    {
        "standard_number": "IS 1077",
        "title": "Common Burnt Clay Building Bricks",
        "short_description": "Classification and specifications for standard fired clay bricks.",
        "status": "CURRENT",
        "sector_id": "SEC-CIVIL",
        "category_id": "CAT-BRICKS",
        "scope_text": "Lays down requirements for dimensions, strength, and water absorption of common burnt clay building bricks.",
        "included_products": ["Clay bricks", "Red bricks", "Building bricks"],
        "excluded_products": ["Fly ash bricks", "Concrete blocks", "Refractory bricks"],
        "applications": ["Masonry", "Wall construction", "Building construction"]
    },
    {
        "standard_number": "IS 2062",
        "title": "Hot Rolled Medium and High Tensile Structural Steel",
        "short_description": "Standard for structural steel sections like I-beams, channels, and angles.",
        "status": "CURRENT",
        "sector_id": "SEC-CIVIL",
        "category_id": "CAT-STEEL",
        "scope_text": "Covers the requirements for hot rolled medium and high tensile structural steel for general engineering and structural purposes.",
        "included_products": ["Structural steel", "I-beams", "Channels", "Angles", "Steel plates"],
        "excluded_products": ["Reinforcement steel", "Cold formed steel"],
        "applications": ["Steel structures", "Bridges", "Industrial sheds", "Fabrication"]
    },

    # OTHER
    {
        "standard_number": "IS 12818",
        "title": "Unplasticized PVC Screen and Casing Pipes for Bore/Tube Wells",
        "short_description": "Requirements for UPVC casing pipes used in groundwater borewells.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-PIPES",
        "scope_text": "Specifies requirements for ribbed and plain UPVC screen and casing pipes for bore/tube wells.",
        "included_products": ["UPVC casing pipes", "Screen pipes", "Borewell pipes"],
        "excluded_products": ["Plumbing UPVC pipes (IS 4985)"],
        "applications": ["Borewells", "Tube wells", "Groundwater extraction", "Water drilling"]
    },
    {
        "standard_number": "IS 14151-1",
        "title": "Polyethylene Pipes for Sprinkler Irrigation Systems - Part 1: Pipes",
        "short_description": "Specifications for PE (polyethylene) pipes used in agricultural sprinkler systems.",
        "status": "CURRENT",
        "sector_id": "SEC-PLUMB",
        "category_id": "CAT-PIPES",
        "scope_text": "Covers requirements for polyethylene (PE) pipes used for sprinkler irrigation systems.",
        "included_products": ["PE pipes", "HDPE pipes for irrigation", "Sprinkler pipes"],
        "excluded_products": ["Drip irrigation laterals", "Potable water PE pipes"],
        "applications": ["Sprinkler irrigation", "Agriculture", "Landscaping"]
    },
    {
        "standard_number": "IS 996",
        "title": "Single-Phase a.c. Induction Motors for General Purpose",
        "short_description": "Requirements for small single-phase electric motors.",
        "status": "CURRENT",
        "sector_id": "SEC-ELEC",
        "category_id": "CAT-MOTORS",
        "scope_text": "Covers single-phase AC induction motors for general purpose applications.",
        "included_products": ["Single-phase motors", "FHP motors", "Capacitor start motors"],
        "excluded_products": ["Three-phase motors", "Special purpose motors"],
        "applications": ["Domestic appliances", "Small water pumps", "Blowers", "Light machinery"]
    },
    {
        "standard_number": "IS 15652",
        "title": "Insulating Mats for Electrical Purposes",
        "short_description": "Specifications for electrical rubber mats used in front of switchboards.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Covers insulating mats made of elastomer (rubber or plastics) intended for use as floor covering for the electrical protection of workers.",
        "included_products": ["Electrical insulating mats", "Switchboard mats", "Safety mats"],
        "excluded_products": ["General purpose rubber mats"],
        "applications": ["Electrical substations", "Switchgear rooms", "Control panels", "Electrical safety"]
    },
    {
        "standard_number": "IS 10592",
        "title": "Industrial Emergency Showers and Eyewash Fountains",
        "short_description": "Requirements for emergency safety showers and eyewash stations in chemical handling areas.",
        "status": "CURRENT",
        "sector_id": "SEC-SAFE",
        "category_id": "CAT-PPE",
        "scope_text": "Specifies requirements for the design, performance, and installation of industrial emergency showers and eyewash fountains.",
        "included_products": ["Emergency showers", "Eyewash fountains", "Safety showers"],
        "excluded_products": ["Standard plumbing fixtures"],
        "applications": ["Chemical plants", "Laboratories", "Battery rooms", "Hazardous material handling"]
    }
]

file_path = 'knowledge_base/seed/standards.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add new categories
existing_cat_ids = {c['id'] for c in data['categories']}
for cat in new_categories:
    if cat['id'] not in existing_cat_ids:
        data['categories'].append(cat)

# Add standards
for std in standards_to_add:
    new_std = {
        "id": str(uuid.uuid4()),
        "standard_number": std["standard_number"],
        "title": std["title"],
        "short_description": std["short_description"],
        "status": std["status"],
        "sector_id": std["sector_id"],
        "category_id": std["category_id"]
    }
    data['standards'].append(new_std)
    
    # scope
    data['standard_scopes'].append({
        "id": str(uuid.uuid4()),
        "standard_id": new_std["id"],
        "scope_text": std["scope_text"],
        "included_products": std["included_products"],
        "excluded_products": std["excluded_products"],
        "applications": std["applications"]
    })
    
    # source (BIS Official)
    data['standard_sources'].append({
        "id": str(uuid.uuid4()),
        "standard_id": new_std["id"],
        "organization": "Bureau of Indian Standards",
        "source_type": "official",
        "source_title": "BIS Catalog",
        "url": f"https://standardsbis.bsbedge.com/",
        "retrieved_date": datetime.datetime.now().isoformat()
    })

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Successfully added {len(standards_to_add)} standards.")
print(f"Total standards now: {len(data['standards'])}")
