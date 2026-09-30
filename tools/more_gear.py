# Generates the extra gear entries for gear.html (between the GEN-MORE markers).
# Rows are compact; descriptions come from per-category templates.
# Prices are approximate Thai street prices (THB); specs are approximate.
# Python 3.5 compatible (no f-strings).
import json, re, sys

KB = """
Gravastar|Mercury K1 Pro|75%|3990|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Gravastar|Mercury K1 Lite|75%|2690|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
MCHOSE|Ace 68|65%|2490|0|he|Magnetic Hall effect|USB-C wired
MCHOSE|Ace 60 Pro|60%|2290|0|he|Magnetic Hall effect|USB-C wired
MCHOSE|Jet 75|75%|3290|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
MCHOSE|GX87|TKL|2990|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
MCHOSE|K7 Ultra|75%|3590|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Attack Shark|X65HE|65%|1990|0|he|Magnetic Hall effect|USB-C wired
Attack Shark|X68HE|65%|2290|0|he|Magnetic Hall effect|USB-C wired
Attack Shark|X85HE|75%|2690|0|he|Magnetic Hall effect|USB-C wired
Attack Shark|K86|75%|1690|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Attack Shark|K85|75%|1490|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
VGN|S99|96% / 98%|2590|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
VGN|N75|75%|2190|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
VGN|V87|TKL|2490|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Ajazz|AK820 Pro|75%|1690|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Ajazz|AK870|TKL|1790|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Ajazz|AK680 MAX|65%|1890|0|he|Magnetic Hall effect|USB-C wired
Aula|F75|75%|1990|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Aula|F99|96% / 98%|2290|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
Aula|F87 Pro|TKL|2190|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
MonsGeek|M1 V5|75%|3490|1|mech|Hot-swap mechanical (linear)|2.4 GHz, Bluetooth, USB-C
MonsGeek|FUN60 Pro|60%|1890|0|he|Magnetic Hall effect|USB-C wired
Madlions|MAD60 HE|60%|1990|0|he|Magnetic Hall effect|USB-C wired
Madlions|MAD68 HE|65%|2290|0|he|Magnetic Hall effect|USB-C wired
Leobog|Hi75|75%|1790|0|mech|Hot-swap mechanical (linear)|USB-C wired
Keychron|K8 Pro|TKL|3690|1|mech|Hot-swap Gateron mechanical|Bluetooth, USB-C
Keychron|V1|75%|2990|0|mech|Hot-swap Keychron K Pro mechanical|USB-C wired
Keychron|Q1 HE|75%|7490|1|he|Gateron magnetic Hall effect|2.4 GHz, Bluetooth, USB-C
Keychron|K2 HE|75%|5290|1|he|Gateron magnetic Hall effect|2.4 GHz, Bluetooth, USB-C
Keychron|K6 Pro|65%|3290|1|mech|Hot-swap Gateron mechanical|Bluetooth, USB-C
Wooting|80HE|75%|7990|0|he|Lekker magnetic Hall effect|USB-C wired
Wooting|Two HE|Full size|7490|0|he|Lekker magnetic Hall effect|USB-C wired
Razer|Huntsman Mini|60%|3490|0|opt|Razer optical (clicky or linear)|USB-C wired
Razer|BlackWidow V4 75%|75%|7290|0|mech|Hot-swap Razer mechanical (tactile)|USB-C wired
Razer|Huntsman V3 Pro Mini|60%|6490|0|he|Razer Analog Optical Gen-2|USB-C wired
Razer|BlackWidow V4 X|Full size|4490|0|mech|Razer mechanical (green or yellow)|USB wired
Logitech G|G915 TKL|TKL|7990|1|mech|GL low-profile mechanical|Lightspeed, Bluetooth
Logitech G|G515 TKL Lightspeed|TKL|5990|1|mech|Low-profile mechanical|Lightspeed, Bluetooth, USB-C
Logitech G|G413 SE|Full size|2290|0|mech|Mechanical (tactile)|USB wired
SteelSeries|Apex 3 TKL|TKL|1990|0|mem|Whisper-quiet membrane|USB wired
SteelSeries|Apex Pro Mini|60%|6990|0|he|OmniPoint 2.0 adjustable (Hall effect)|USB-C wired
SteelSeries|Apex 9 TKL|TKL|4990|0|opt|OptiPoint optical|USB-C wired
Corsair|K65 Plus Wireless|75%|5490|1|mech|Hot-swap Corsair MLX (linear)|Slipstream 2.4 GHz, Bluetooth, USB-C
Corsair|K100 RGB|Full size|8990|0|opt|Corsair OPX optical|USB wired
Corsair|K70 Pro Mini Wireless|60%|5990|1|mech|Hot-swap Cherry MX|Slipstream 2.4 GHz, Bluetooth, USB-C
HyperX|Alloy Origins 60|60%|2990|0|mech|HyperX mechanical (linear)|USB-C wired
HyperX|Alloy Rise 75|75%|5490|0|mech|Hot-swap HyperX mechanical (linear)|USB-C wired
ASUS ROG|Falchion RX Low Profile|65%|4990|1|opt|ROG RX low-profile optical|2.4 GHz, Bluetooth, USB-C
ASUS ROG|Strix Scope II 96 Wireless|96% / 98%|5990|1|mech|Hot-swap ROG NX mechanical|2.4 GHz, Bluetooth, USB-C
ASUS ROG|Falchion Ace HFX|65%|5490|0|he|ROG HFX magnetic Hall effect|USB-C wired
Akko|3068B Plus|65%|2290|1|mech|Hot-swap Akko CS mechanical|2.4 GHz, Bluetooth, USB-C
Akko|MOD007B HE|65%|3990|1|he|Akko magnetic Hall effect|2.4 GHz, Bluetooth, USB-C
Akko|3098B|96% / 98%|2590|1|mech|Hot-swap Akko CS mechanical|2.4 GHz, Bluetooth, USB-C
Royal Kludge|RK84|75%|1590|1|mech|Hot-swap mechanical|2.4 GHz, Bluetooth, USB-C
Royal Kludge|RK100|96% / 98%|1890|1|mech|Hot-swap mechanical|2.4 GHz, Bluetooth, USB-C
Epomaker|TH80 Pro|75%|2790|1|mech|Hot-swap Gateron mechanical|2.4 GHz, Bluetooth, USB-C
NuPhy|Air75 V2|75%|4290|1|mech|Low-profile Gateron mechanical|2.4 GHz, Bluetooth, USB-C
NuPhy|Halo75 V2|75%|4690|1|mech|Hot-swap NuPhy mechanical|2.4 GHz, Bluetooth, USB-C
DrunkDeer|A75|75%|2990|0|he|Magnetic Hall effect|USB-C wired
Leopold|FC900R PD|Full size|4490|0|mech|Cherry MX|USB wired
Leopold|FC750R PD|TKL|4290|0|mech|Cherry MX|USB wired
Leopold|FC660M PD|65%|3990|0|mech|Cherry MX|USB wired
Varmilo|VA87M|TKL|4590|0|mech|Varmilo EC or Cherry MX|USB-C wired
Ducky|One 3 Full|Full size|4590|0|mech|Hot-swap Cherry MX|USB-C wired
Ducky|One 3 TKL|TKL|4290|0|mech|Hot-swap Cherry MX|USB-C wired
Ducky|One 3 SF|65%|3990|0|mech|Hot-swap Cherry MX|USB-C wired
Ducky|One 3 Mini|60%|3790|0|mech|Hot-swap Cherry MX|USB-C wired
Redragon|K617 Fizz|60%|990|0|mech|Hot-swap Redragon mechanical|USB-C wired
Redragon|K630 Dragonborn|65%|1090|0|mech|Hot-swap Redragon mechanical|USB-C wired
Redragon|K556 Devarajas|Full size|1690|0|mech|Hot-swap Redragon mechanical|USB wired
Fantech|MAXFIT61|60%|1290|0|mech|Hot-swap mechanical|USB-C wired
Logitech|K380 Multi-Device|65%|1190|1|mem|Low-profile scissor (membrane)|Bluetooth
"""

MS = """
Gravastar|Mercury M1 Pro|Ultralight|2490|1|~65 g (honeycomb)|PixArt PAW3395|up to 4,000 Hz
Gravastar|Mercury M1 Lite|Ultralight|1490|1|~70 g (honeycomb)|PixArt PAW3311|1,000 Hz
Gravastar|Mercury M2 Pro|Ultralight|2790|1|~60 g (honeycomb)|PixArt PAW3395|up to 4,000 Hz
MCHOSE|A5 Pro|Ultralight|1290|1|~50 g|PixArt PAW3395|1,000 Hz
MCHOSE|A5 Pro Max|Ultralight|1790|1|~50 g|PixArt PAW3950|up to 8,000 Hz
MCHOSE|A5 Ultra|Ultralight|2190|1|~48 g|PixArt PAW3950|up to 8,000 Hz
MCHOSE|L7 Pro|Ultralight|1490|1|~55 g|PixArt PAW3395|1,000 Hz
MCHOSE|L7 Ultra|Ultralight|2290|1|~52 g|PixArt PAW3950|up to 8,000 Hz
MCHOSE|G3 Ultra|Ergonomic|2190|1|~58 g|PixArt PAW3950|up to 8,000 Hz
Attack Shark|X11|Budget|790|1|~61 g|PixArt PAW3311|1,000 Hz
Attack Shark|X3|Ultralight|990|1|~49 g|PixArt PAW3395|1,000 Hz
Attack Shark|X3 Pro|Ultralight|1490|1|~50 g|PixArt PAW3395|up to 8,000 Hz
Attack Shark|R1|Ultralight|1090|1|~55 g|PixArt PAW3311|1,000 Hz
Attack Shark|R5 Ultra|Ultralight|1990|1|~40 g|PixArt PAW3950|up to 8,000 Hz
Attack Shark|X6|Ultralight|990|1|~49 g|PixArt PAW3395|1,000 Hz
Attack Shark|X5 Pro|Ergonomic|1290|1|~58 g|PixArt PAW3395|1,000 Hz
VXE|R1|Budget|890|1|~55 g|PixArt PAW3395|1,000 Hz
VXE|R1 Pro|Ultralight|1190|1|~50 g|PixArt PAW3395|1,000 Hz
VXE|R1 Pro Max|Ultralight|1590|1|~50 g|PixArt PAW3395|up to 4,000 Hz
VXE|Dragonfly F1 Pro|Ultralight|1490|1|~50 g|PixArt PAW3395|1,000 Hz
VXE|Dragonfly F1 Pro Max|Ultralight|1890|1|~50 g|PixArt PAW3395|up to 4,000 Hz
VXE|MAD R Major|Ultralight|2290|1|~36 g|PixArt PAW3950|up to 8,000 Hz
Darmoshark|M3|Ultralight|1290|1|~55 g|PixArt PAW3395|1,000 Hz
Darmoshark|N3|Ultralight|1490|1|~55 g|PixArt PAW3395|up to 4,000 Hz
Lamzu|Atlantis Mini 4K|Ultralight|3290|1|~51 g|PixArt PAW3395|up to 4,000 Hz
Lamzu|Maya X|Ultralight|3690|1|~47 g|PixArt PAW3950|up to 8,000 Hz
Lamzu|Thorn|Ergonomic|3290|1|~53 g|PixArt PAW3395|up to 4,000 Hz
Finalmouse|UltralightX|Ultralight|6990|1|~38 g (carbon fibre)|Finalsensor|up to 8,000 Hz
Endgame Gear|OP1 8K|Ultralight|2490|0|~50 g|PixArt PAW3395|up to 8,000 Hz
Endgame Gear|XM2we|Ultralight|2790|1|~63 g|PixArt PAW3370|1,000 Hz
Ninjutso|Sora V2|Ultralight|3690|1|~40 g|PixArt PAW3395|up to 4,000 Hz
Zowie|EC2-CW|Ergonomic|4990|1|~77 g|Zowie 3370 optical|up to 4,000 Hz
Zowie|FK2-C|Ultralight|2590|0|~73 g|Zowie 3360 optical|1,000 Hz
Zowie|S2-C|Ultralight|2590|0|~73 g|Zowie 3360 optical|1,000 Hz
Zowie|ZA13-C|Ultralight|2590|0|~65 g|Zowie 3360 optical|1,000 Hz
Pulsar|Xlite V3|Ergonomic|3490|1|~55 g|PixArt PAW3395|up to 4,000 Hz
Pulsar|X2H|Ultralight|3290|1|~52 g|PixArt PAW3395|up to 4,000 Hz
Logitech G|PRO X Superlight|Ultralight|3990|1|~63 g|HERO 25K|1,000 Hz
Logitech G|PRO Wireless|Ultralight|3490|1|~80 g|HERO 25K|1,000 Hz
Logitech G|G703 Lightspeed|Ergonomic|2690|1|~95 g|HERO 25K|1,000 Hz
Logitech G|G502 Hero|Multi-button|1590|0|~121 g (adjustable)|HERO 25K|1,000 Hz
Logitech G|G309 Lightspeed|Budget|1790|1|~68 g (AA battery)|HERO 25K|1,000 Hz
Logitech G|G502 Lightspeed|Multi-button|3990|1|~114 g|HERO 25K|1,000 Hz
Razer|Viper V3 HyperSpeed|Ultralight|2590|1|~82 g|Razer Focus X 26K|1,000 Hz
Razer|DeathAdder Essential|Budget|690|0|~96 g|Optical 6,400 DPI|1,000 Hz
Razer|DeathAdder V3|Ergonomic|2690|0|~59 g|Razer Focus Pro 30K|up to 8,000 Hz
Razer|Cobra Pro|Ultralight|4490|1|~77 g|Razer Focus Pro 30K|1,000 Hz
Razer|Orochi V2|Budget|1790|1|~60 g (without battery)|Razer 5G optical|1,000 Hz
Razer|Basilisk V3 Pro|Multi-button|5490|1|~112 g|Razer Focus Pro 30K|1,000 Hz
Razer|Naga V2 Pro|Multi-button|5990|1|~134 g|Razer Focus Pro 30K|1,000 Hz
SteelSeries|Rival 3|Budget|990|0|~77 g|TrueMove Core|1,000 Hz
SteelSeries|Aerox 3 Wireless|Ultralight|2990|1|~68 g|TrueMove Air|1,000 Hz
SteelSeries|Prime Wireless|Ultralight|3490|1|~80 g|TrueMove Air|1,000 Hz
HyperX|Pulsefire Haste 2|Ultralight|1590|0|~53 g|HyperX 26K|up to 8,000 Hz
HyperX|Pulsefire Haste 2 Wireless|Ultralight|2590|1|~61 g|HyperX 26K|1,000 Hz
Corsair|Sabre RGB Pro|Ultralight|1790|0|~74 g|Corsair Marksman|up to 8,000 Hz
Corsair|Dark Core RGB Pro|Ergonomic|3490|1|~133 g|Corsair Marksman|up to 2,000 Hz
Corsair|Harpoon RGB Wireless|Budget|1490|1|~99 g|Optical 10,000 DPI|1,000 Hz
Glorious|Model D 2 Wireless|Ergonomic|3290|1|~68 g|Glorious BAMF 2.0|up to 4,000 Hz
Glorious|Model O 2|Ultralight|1790|0|~59 g|Glorious BAMF 2.0|1,000 Hz
ASUS ROG|Harpe Ace Aim Lab Edition|Ultralight|3990|1|~54 g|ROG AimPoint 36K|1,000 Hz
ASUS ROG|Keris II Ace|Ultralight|4990|1|~54 g|ROG AimPoint Pro 42K|up to 8,000 Hz
ASUS ROG|Gladius III Wireless AimPoint|Ergonomic|3990|1|~79 g|ROG AimPoint 36K|1,000 Hz
Fantech|Helios II Pro XD3V3|Ultralight|1290|1|~57 g|PixArt PAW3395|1,000 Hz
Fantech|Aria XD7|Ultralight|1490|1|~59 g|PixArt PAW3395|1,000 Hz
Rapoo|VT9 Pro|Ultralight|1190|1|~58 g|PixArt PAW3398|1,000 Hz
Redragon|M808 Storm Pro|Budget|890|1|~75 g (honeycomb)|PixArt PAW3325|1,000 Hz
Logitech|MX Master 3S|Ergonomic|3990|1|~141 g|Darkfield 8K|125 Hz
"""

HS = """
Gravastar|Sirius Pro|Earbuds / IEM|2490|1|10 mm dynamic|Up to 7 hours (earbuds)|Bluetooth 5.3
Razer|Kraken V4|Wireless|6490|1|40 mm TriForce Bio-Cellulose|Up to 70 hours|HyperSpeed 2.4 GHz, Bluetooth, USB
Razer|Kraken V3 X|Wired|1990|0|40 mm TriForce|-|USB
Razer|BlackShark V2 HyperSpeed|Wireless|3990|1|50 mm TriForce Bio-Cellulose|Up to 70 hours|HyperSpeed 2.4 GHz, Bluetooth
Razer|Barracuda X|Wireless|3490|1|40 mm TriForce|Up to 50 hours|2.4 GHz USB-C, Bluetooth
Razer|Hammerhead Pro HyperSpeed|Earbuds / IEM|6990|1|10 mm dynamic|Up to 30 hours with case|HyperSpeed 2.4 GHz, Bluetooth
Logitech G|G435 Lightspeed|Wireless|1990|1|40 mm|Up to 18 hours|Lightspeed 2.4 GHz, Bluetooth
Logitech G|G733 Lightspeed|Wireless|4290|1|40 mm PRO-G|Up to 29 hours|Lightspeed 2.4 GHz
Logitech G|G335|Wired|1690|0|40 mm|-|3.5 mm
Logitech G|PRO X Wired|Wired|3990|0|50 mm PRO-G|-|3.5 mm, USB DAC
Logitech G|FITS True Wireless|Earbuds / IEM|6990|1|10 mm dynamic|Up to 7 hours (earbuds)|Lightspeed 2.4 GHz, Bluetooth
SteelSeries|Arctis Nova 7 Wireless|Wireless|6490|1|40 mm Nova|Up to 38 hours|2.4 GHz, Bluetooth
SteelSeries|Arctis Nova 5 Wireless|Wireless|4490|1|40 mm Nova|Up to 60 hours|2.4 GHz, Bluetooth
SteelSeries|Arctis Nova 3|Wired|2490|0|40 mm Nova|-|USB-C, 3.5 mm
SteelSeries|Arctis Nova Pro Wired|Wired|8490|0|40 mm Nova Pro|-|USB with GameDAC
HyperX|Cloud II|Wired|2690|0|53 mm|-|3.5 mm, USB sound card
HyperX|Cloud Stinger 2|Wired|1290|0|50 mm|-|3.5 mm
HyperX|Cloud III Wireless|Wireless|4990|1|53 mm angled|Up to 120 hours|2.4 GHz USB-C
HyperX|Cloud Alpha|Wired|2990|0|50 mm dual-chamber|-|3.5 mm
Corsair|HS80 RGB Wireless|Wireless|4990|1|50 mm neodymium|Up to 20 hours|Slipstream 2.4 GHz
Corsair|Virtuoso RGB Wireless XT|Wireless|8490|1|50 mm high-density|Up to 15 hours|Slipstream 2.4 GHz, Bluetooth, USB, 3.5 mm
Corsair|HS55 Stereo|Wired|1790|0|50 mm neodymium|-|3.5 mm
Sony|INZONE H3|Wired|2490|0|40 mm|-|3.5 mm
Sony|INZONE H5|Wireless|4990|1|40 mm|Up to 28 hours|2.4 GHz USB-C, 3.5 mm
Sony|INZONE Buds|Earbuds / IEM|6990|1|8.4 mm dynamic|Up to 12 hours (earbuds)|2.4 GHz USB-C dongle, Bluetooth LE
Turtle Beach|Stealth 600 Gen 3|Wireless|3990|1|50 mm Eclipse|Up to 80 hours|2.4 GHz, Bluetooth
Turtle Beach|Stealth Pro|Wireless|10990|1|50 mm Nanoclear|Up to 12 hours per battery (hot-swap)|2.4 GHz, Bluetooth
EPOS|H6PRO Open|Wired|5490|0|42 mm|-|3.5 mm
ASUS ROG|Delta S|Wired|4990|0|50 mm ASUS Essence|-|USB-C
ASUS ROG|Cetra True Wireless Pro|Earbuds / IEM|4490|1|10 mm dynamic|Up to 7 hours (earbuds)|Bluetooth, USB-C
JBL|Quantum 910 Wireless|Wireless|7490|1|50 mm|Up to 39 hours|2.4 GHz, Bluetooth, USB
JBL|Quantum 100|Wired|890|0|40 mm|-|3.5 mm
Sennheiser|HD 560S|Studio|6990|0|38 mm dynamic, open-back|-|6.3 mm / 3.5 mm
Audio-Technica|ATH-M50x|Studio|5490|0|45 mm, closed-back|-|3.5 mm (detachable)
Audio-Technica|ATH-M40x|Studio|3990|0|40 mm, closed-back|-|3.5 mm (detachable)
Philips|SHP9500|Studio|2990|0|50 mm, open-back|-|3.5 mm (detachable)
AKG|K371|Studio|4990|0|50 mm, closed-back|-|3.5 mm (detachable)
beyerdynamic|DT 900 PRO X|Studio|8990|0|45 mm STELLAR.45, open-back|-|3.5 mm (detachable)
KZ|ZSN Pro X|Earbuds / IEM|790|0|Hybrid 1 dynamic + 1 balanced armature|-|3.5 mm (detachable)
Truthear|Zero:Red|Earbuds / IEM|1890|0|Dual dynamic|-|3.5 mm (detachable)
Tanchjim|Zero|Earbuds / IEM|590|0|10 mm dynamic|-|3.5 mm
7Hz|Salnotes Zero|Earbuds / IEM|790|0|10 mm dynamic|-|3.5 mm (detachable)
Moondrop|Aria 2|Earbuds / IEM|2990|0|10 mm dynamic|-|3.5 mm (detachable)
Moondrop|Space Travel|Earbuds / IEM|790|1|13 mm dynamic|Up to 6 hours (earbuds)|Bluetooth 5.3
"""

MON = """
AOC|24G4|1080p|4390|23.8"|1920 × 1080|180|Fast IPS
AOC|25G3ZM|1080p|4790|24.5"|1920 × 1080|240|VA
AOC|Q27G4X|1440p|7490|27"|2560 × 1440|180|Fast IPS
ASUS|TUF Gaming VG259QM|1080p|7490|24.5"|1920 × 1080|280|Fast IPS
ASUS|TUF Gaming VG27AQ3A|1440p|7990|27"|2560 × 1440|180|Fast IPS
ASUS ROG|Strix XG27ACS|1440p|10990|27"|2560 × 1440|180|Fast IPS
ASUS ROG|Swift PG27AQN|1440p|32900|27"|2560 × 1440|360|Fast IPS
ASUS ROG|Swift PG34WCDM|Ultrawide|36900|34" curved|3440 × 1440|240|WOLED
MSI|G255F|1080p|4290|24.5"|1920 × 1080|180|Rapid IPS
MSI|MPG 271QRX QD-OLED|1440p|27900|26.5"|2560 × 1440|360|QD-OLED
MSI|MPG 321URX QD-OLED|4K|37900|31.5"|3840 × 2160|240|QD-OLED
MSI|MAG 341CQP QD-OLED|Ultrawide|25900|34" curved|3440 × 1440|175|QD-OLED
Samsung|Odyssey G5 (G51C)|1440p|7990|27"|2560 × 1440|165|VA
Samsung|Odyssey G7 (G70B)|4K|19900|28"|3840 × 2160|144|IPS
Samsung|Odyssey OLED G8 (G80SD)|4K|39900|32"|3840 × 2160|240|QD-OLED
LG|UltraGear 24GS60F|1080p|4290|23.8"|1920 × 1080|180|IPS
LG|UltraGear 27GR75Q|1440p|8490|27"|2560 × 1440|165|IPS
LG|UltraGear 27GS95QE|1440p|28900|26.5"|2560 × 1440|240|WOLED
LG|UltraGear 45GR95QE|Ultrawide|49900|45" curved|3440 × 1440|240|WOLED
Gigabyte|G24F 2|1080p|4490|23.8"|1920 × 1080|180|SS IPS
Gigabyte|M27Q (rev. 2.0)|1440p|8490|27"|2560 × 1440|170|SS IPS
Gigabyte|AORUS FO27Q3|1440p|26900|27"|2560 × 1440|360|QD-OLED
Gigabyte|M32U|4K|19900|31.5"|3840 × 2160|144|SS IPS
Gigabyte|G34WQC A|Ultrawide|11900|34" curved|3440 × 1440|144|VA
Dell|G2724D|1440p|8990|27"|2560 × 1440|165|Fast IPS
Dell|S2721DGF|1440p|11990|27"|2560 × 1440|165|Nano IPS
Alienware|AW3423DWF|Ultrawide|29900|34" curved|3440 × 1440|165|QD-OLED
Alienware|AW3225QF|4K|39900|31.6" curved|3840 × 2160|240|QD-OLED
Alienware|AW2524H|1080p|24900|24.5"|1920 × 1080|500|Fast IPS
Zowie|XL2546K|1080p|16900|24.5"|1920 × 1080|240|TN (DyAc+)
Zowie|XL2546X|1080p|22900|24.5"|1920 × 1080|240|Fast TN (DyAc 2)
BenQ|MOBIUZ EX2710Q|1440p|12900|27"|2560 × 1440|165|IPS
BenQ|MOBIUZ EX3210U|4K|29900|32"|3840 × 2160|144|IPS
Acer|Nitro XV272U V3|1440p|7990|27"|2560 × 1440|180|IPS
Acer|Predator XB273K V3|4K|21900|27"|3840 × 2160|160|IPS
Acer|Nitro VG240Y M3|1080p|3690|23.8"|1920 × 1080|180|IPS
KTC|H27T22|1440p|5990|27"|2560 × 1440|165|Fast IPS
Xiaomi|Gaming Monitor G27i|1080p|4290|27"|1920 × 1080|165|Fast IPS
Xiaomi|Curved Gaming Monitor 34|Ultrawide|9990|34" curved|3440 × 1440|180|VA
ViewSonic|VX2728J-2K|1440p|6490|27"|2560 × 1440|180|Fast IPS
"""

ACC = """
Artisan|Hien FX (XL)|Mouse pad|3290|0|Surface|Balanced, textured cloth
Artisan|Zero FX (XL)|Mouse pad|3290|0|Surface|Control-leaning cloth
Lethal Gaming Gear|Saturn Pro|Mouse pad|1890|0|Surface|Control cloth, flat stitched edges
Razer|Strider (XXL)|Mouse pad|1690|0|Surface|Hybrid cloth, water resistant
Glorious|Mouse Pad XL Extended|Mouse pad|990|0|Surface|Smooth cloth, stitched edges
SteelSeries|QcK Prism Cloth (XL)|Mouse pad|1990|0|Surface|Cloth with two-zone RGB
Pulsar|ParaBrake (XL)|Mouse pad|1490|0|Surface|Control-focused cloth
Zowie|G-SR II|Mouse pad|1690|0|Surface|Rubber base, control cloth
X-raypad|Aqua Control Plus|Mouse pad|1290|0|Surface|Balanced cloth, stitched edges
Attack Shark|Speed Pad (XL)|Mouse pad|490|0|Surface|Smooth speed cloth
Gravastar|Mercury Mouse Pad (XL)|Mouse pad|890|0|Surface|Smooth cloth
Logitech G|G840 XL|Mouse pad|1590|0|Surface|Medium-friction cloth
Xbox|Elite Wireless Controller Series 2|Controller|5990|1|Features|Adjustable-tension sticks, paddles, 40-hour battery
PlayStation|DualSense Edge|Controller|7490|1|Features|Swappable sticks, back buttons, trigger stops
8BitDo|Ultimate 2C Wireless|Controller|990|1|Features|2.4 GHz, Hall effect sticks, extra bumpers
8BitDo|Ultimate 2 Wireless|Controller|2190|1|Features|TMR sticks, charging dock, 2.4 GHz and Bluetooth
GameSir|G7 SE|Controller|1690|0|Features|Wired Xbox-licensed, Hall effect sticks
GameSir|Nova Lite|Controller|890|1|Features|Hall effect sticks, 2.4 GHz and Bluetooth
Razer|Wolverine V2 Chroma|Controller|5490|0|Features|Wired, Mecha-Tactile face buttons, back paddles
Flydigi|Vader 4 Pro|Controller|2990|1|Features|Force-feedback triggers, back buttons, 2.4 GHz
Nintendo|Switch Pro Controller|Controller|2490|1|Features|Bluetooth, up to 40-hour battery
Fifine|AmpliGame A8|Microphone|1290|0|Type|USB condenser, RGB, mute tap
Fifine|K669B|Microphone|990|0|Type|USB condenser
Maono|PD200X|Microphone|2490|0|Type|Dynamic, USB + XLR
HyperX|SoloCast|Microphone|1690|0|Type|USB condenser, tap-to-mute
Razer|Seiren Mini|Microphone|1590|0|Type|USB condenser, supercardioid
RODE|NT-USB Mini|Microphone|3990|0|Type|USB condenser
RODE|PodMic USB|Microphone|6990|0|Type|Dynamic, USB + XLR
Elgato|Wave:3|Microphone|5490|0|Type|USB condenser, Clipguard
Shure|MV6|Microphone|4290|0|Type|USB-C dynamic
Audio-Technica|AT2020USB-X|Microphone|4990|0|Type|USB-C condenser
Logitech G|Yeti GX|Microphone|5490|0|Type|USB dynamic, supercardioid
Logitech|C922 Pro Stream|Webcam|2890|0|Resolution|1080p30 / 720p60
Logitech|Brio 500|Webcam|4490|0|Resolution|1080p30, auto light correction
Logitech|Brio 4K|Webcam|6990|0|Resolution|4K30 / 1080p60, HDR
Razer|Kiyo Pro|Webcam|5490|0|Resolution|1080p60, HDR, large sensor
Elgato|Facecam|Webcam|4990|0|Resolution|1080p60, uncompressed
OBSBOT|Tiny 2|Webcam|10990|0|Resolution|4K30, AI auto-tracking gimbal
Insta360|Link|Webcam|9990|0|Resolution|4K30, AI tracking gimbal
Elgato|Stream Deck Mini|Stream control|2990|0|Controls|6 LCD keys
Elgato|Stream Deck +|Stream control|6990|0|Controls|8 LCD keys, 4 dials, touch strip
Elgato|Stream Deck XL|Stream control|8490|0|Controls|32 LCD keys
Elgato|HD60 X|Stream control|5990|0|Controls|Capture card, 4K30 HDR passthrough
Elgato|Cam Link 4K|Stream control|3990|0|Controls|Use a camera as a webcam over HDMI
TC Helicon|GoXLR Mini|Stream control|6990|0|Controls|4-channel USB mixer for streaming
Anda Seat|Kaiser 3 (L)|Chair|15900|0|Build|Steel frame, PVC leather, 4D armrests
Herman Miller|Vantum Gaming Chair|Chair|29900|0|Build|Ergonomic shell, posture-first design
Razer|Iskur V2|Chair|19900|0|Build|Adaptive lumbar support, 4D armrests
Corsair|TC100 Relaxed|Chair|7990|0|Build|Wide seat, fabric or leatherette
Noblechairs|Hero|Chair|15900|0|Build|Steel frame, integrated lumbar adjust
Cougar|Armor One|Chair|4990|0|Build|Budget steel frame, breathable leatherette
DXRacer|Formula Series|Chair|8990|0|Build|Racing style, PU leather
"""

KB_T = {
 'he': ('Magnetic switches with adjustable actuation and Rapid Trigger, so keys reset the moment you lift. Great for fast strafing in FPS games.',
        ['Rapid Trigger and adjustable actuation','Very fast, consistent key response'],['Needs software to tune per-key settings']),
 'mech':('A mechanical keyboard with a satisfying, reliable feel for both gaming and typing.',
        ['Solid mechanical feel','Easy to customise with keycaps'],['No Rapid Trigger like magnetic boards']),
 'opt': ('Optical switches register a press with light instead of metal contacts, so they are fast and very durable.',
        ['Fast optical actuation','Durable switches'],['Fewer switch options than standard mechanical']),
 'mem': ('A quiet, budget-friendly board that is easy to live with for everyday gaming and work.',
        ['Quiet and affordable','Spill-friendly and simple'],['Softer, less crisp feel than mechanical']),
}
SIZE_NOTE = {'60%':'The tiny 60% layout leaves loads of room for big mouse swipes.',
 '65%':'A 65% layout keeps arrow keys while staying very compact.',
 '75%':'A 75% layout keeps the function row and arrows in a compact footprint.',
 'TKL':'Tenkeyless drops the number pad for more mouse room.',
 'Full size':'Full size includes the number pad for work and spreadsheets.',
 '96% / 98%':'A 96/98% layout squeezes in a number pad while saving desk space.'}
MS_T = {'Ultralight':'A light, fast mouse built for quick flicks and tracking in shooters.',
 'Ergonomic':'A right-handed ergonomic shape that suits relaxed palm grip for long sessions.',
 'Multi-button':'Extra programmable buttons for MMOs, MOBAs, macros and productivity.',
 'Budget':'An affordable pick that still gets the basics right for gaming.'}
HS_T = {'Wireless':'A wireless headset with long battery life and freedom from cables.',
 'Wired':'A wired headset: no charging, no lag, just plug in and play.',
 'Earbuds / IEM':'In-ear audio: light, portable and great for hearing footsteps.',
 'Studio':'Studio headphones with accurate sound; pair with a separate mic for gaming.'}
ACC_T = {'Mouse pad':'A gaming surface that sets how your mouse glides and stops.',
 'Controller':'A controller for PC and console games that feel better on sticks.',
 'Microphone':'A microphone that makes you sound clear on Discord, calls and stream.',
 'Webcam':'Desk gear that upgrades your stream, calls or setup.',
 'Stream control':'Tools that make streaming and content creation easier.',
 'Chair':'A chair built for long gaming and study sessions.'}

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

out, seen = [], set()
def add(cat, brand, name, sub, price, wl, spec, desc, pros, cons, best):
    pid = 'x-' + slug(brand + ' ' + name)
    if pid in seen:
        sys.exit('duplicate id ' + pid)
    seen.add(pid)
    out.append({'id':pid,'cat':cat,'sub':sub,'brand':brand,'name':name,'price':int(price),'wl':wl=='1',
                'spec':spec,'desc':desc,'pros':pros,'cons':cons,'best':best})

def rows(block):
    return [l.split('|') for l in block.strip().split('\n') if l.strip()]

for b,n,sub,pr,wl,kind,sw,conn in rows(KB):
    d,p,c = KB_T[kind]
    act = [['Actuation','Adjustable, Rapid Trigger']] if kind=='he' else []
    add('keyboard',b,n,sub,pr,wl,[['Size',sub],['Switches',sw]]+act+[['Connection',conn]],
        d+' '+SIZE_NOTE[sub],p+([ 'Wireless freedom'] if wl=='1' else ['Plug-and-play wired']),
        c+([] if wl=='1' else ['Wired only']),
        ('FPS players who want Rapid Trigger' if kind=='he' else 'Gamers who want a '+sub+' '+('wireless ' if wl=='1' else '')+'board')+' from '+b+'.')

for b,n,sub,pr,wl,w,sen,poll in rows(MS):
    add('mouse',b,n,sub,pr,wl,[['Weight',w],['Sensor',sen],['Polling rate',poll],['Connection','2.4 GHz wireless + USB-C' if wl=='1' else 'USB wired']],
        MS_T[sub]+' Uses a '+sen+' sensor at '+poll+'.',
        ['Weighs '+w.replace('~','about '),'Reliable '+sen+' sensor'],
        ['Shape is personal: try one if you can'] + (['Needs charging'] if wl=='1' else ['Cable adds some drag']),
        sub+' '+('wireless ' if wl=='1' else '')+'mouse shoppers'+(' on a budget' if int(pr)<1500 else '')+'.')

for b,n,sub,pr,wl,drv,bat,conn in rows(HS):
    spec=[['Type',sub],['Drivers',drv],['Connection',conn]]
    if bat!='-': spec.append(['Battery',bat])
    add('headset',b,n,sub,pr,wl,spec,HS_T[sub],
        ['Good sound for the price' if int(pr)<3000 else 'Premium sound and build',conn.split(',')[0]+' connection'],
        (['Needs charging'] if wl=='1' else ['Cable to manage'])+(['No built-in mic'] if sub=='Studio' else []),
        ('Listeners who want accurate audio' if sub=='Studio' else 'Gamers who want a '+sub.lower()+' option')+' from '+b+'.')

for b,n,sub,pr,size,res,hz,panel in rows(MON):
    add('monitor',b,n,sub,pr,'0',[['Size',size],['Resolution',res],['Refresh rate',hz+' Hz'],['Panel',panel]],
        'A '+size.replace('"',' inch')+' '+panel+' monitor at '+res+' and '+hz+' Hz.'+(' OLED gives perfect blacks and instant response.' if 'OLED' in panel else ''),
        [hz+' Hz for smooth motion',panel+' panel'],
        (['Watch for burn-in with static screens'] if 'OLED' in panel else [])+(['Needs a strong GPU at this resolution'] if sub in ('4K','Ultrawide') else ['Check the stand and ports suit your desk']),
        {'1080p':'Esports players who want high frame rates on a budget.','1440p':'The sweet spot for sharpness and speed.','4K':'Sharp visuals for story games and work.','Ultrawide':'Sims, racing and multitasking.'}[sub])

for b,n,sub,pr,wl,lab,val in rows(ACC):
    add('accessory',b,n,sub,pr,wl,[[lab,val]],ACC_T[sub]+' '+val+'.',[val.split(',')[0]],['Check current price and stock'],
        'Anyone upgrading their '+sub.lower()+' on the desk.')

sys.stdout.write('/* GEN-MORE start: generated by tools/more_gear.py, approximate specs and prices */\n')
for o in out:
    sys.stdout.write(json.dumps(o, ensure_ascii=False, separators=(',',':')) + ',\n')
sys.stdout.write('/* GEN-MORE end */\n')
sys.stderr.write('%d items\n' % len(out))
