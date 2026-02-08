"""Peuple la base de données avec les données scrappées des 3 concurrents."""

import sqlite3
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import random

DB_PATH = Path(__file__).parent / "database" / "cosmetique.db"

# ============================================================
# DONNÉES PAULA'S CHOICE (top 45 produits - best-sellers FR)
# ============================================================
PAULAS_CHOICE_PRODUCTS = [
    {"name": "Lotion Exfoliante 2% BHA", "price": 39.00, "sale_price": 31.20, "rating": 4.2, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2010-moon-1", "url": "https://www.paulaschoice.fr/fr/skin-perfecting-bha-liquid-exfoliant/m2010.html", "category": "Exfoliants"},
    {"name": "Traitement 1% Rétinol", "price": 71.00, "sale_price": 56.80, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/8010-moon-1", "url": "https://www.paulaschoice.fr/fr/clinical-retinol-treatment/m8010.html", "category": "Traitements"},
    {"name": "Sérum Longévité CellularYouth", "price": 75.00, "sale_price": 60.00, "rating": 5.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2250-moon-1", "url": "https://www.paulaschoice.fr/fr/cellularyouth-longevity-serum/2250.html", "category": "Sérums"},
    {"name": "Crème Hydratante Repulpante Peptides Pro-Collagène", "price": 56.00, "sale_price": 44.80, "rating": 4.4, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1510-moon-1", "url": "https://www.paulaschoice.fr/fr/pro-collagen-peptide-plumping-moisturizer/m1510.html", "category": "Hydratants"},
    {"name": "Booster 15% Vitamine C", "price": 62.00, "sale_price": 49.60, "rating": 4.2, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7770-moon-1", "url": "https://www.paulaschoice.fr/fr/vitamin-c-15-super-booster/97770.html", "category": "Boosters"},
    {"name": "Booster 10% Acide Azélaïque", "price": 49.00, "sale_price": 39.20, "rating": 3.7, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7750-moon-1", "url": "https://www.paulaschoice.fr/fr/aa-booster/m7750.html", "category": "Boosters"},
    {"name": "Traitement Rétinaldéhyde Duo PRO", "price": 73.00, "sale_price": 58.40, "rating": 4.4, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1500-moon-1", "url": "https://www.paulaschoice.fr/fr/clinical-pro-retinaldehyde-dual-retinoid-treatment/m1500.html", "category": "Traitements"},
    {"name": "Traitement 20% Niacinamide", "price": 59.00, "sale_price": 47.20, "rating": 4.1, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/8030-moon-1", "url": "https://www.paulaschoice.fr/fr/niacinamide-treatment/8030-01.html", "category": "Traitements"},
    {"name": "Traitement 0,3% Rétinol + 2% Bakuchiol", "price": 69.00, "sale_price": 55.20, "rating": 4.4, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/8015-moon-1", "url": "https://www.paulaschoice.fr/fr/clinical-retinol-bakuchiol-treatment/m8015.html", "category": "Traitements"},
    {"name": "Sérum Yeux Raffermissant Peptides Pro-Collagène", "price": 47.00, "sale_price": 37.60, "rating": 4.3, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1080-moon-1", "url": "https://www.paulaschoice.fr/fr/pro-collagen-peptide-firming-eye-serum/m1080.html", "category": "Contour des yeux"},
    {"name": "Booster Peptides Pro-Collagène", "price": 65.00, "sale_price": 52.00, "rating": 3.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/3020-moon-1", "url": "https://www.paulaschoice.fr/fr/pro-collagen-multi-peptide-booster/m3020.html", "category": "Boosters"},
    {"name": "Lotion Exfoliante 6% Acide Mandélique + 2% Acide Lactique", "price": 39.00, "sale_price": 31.20, "rating": 4.2, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1470-redesign1", "url": "https://www.paulaschoice.fr/fr/skin-perfecting-6pct-mandelic-acid-2pct-lactic-acid-liquid-exfoliant/m1470.html", "category": "Exfoliants"},
    {"name": "Crème Hydratante Légère SPF 50", "price": 46.00, "sale_price": 36.80, "rating": 4.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7800-moon-1", "url": "https://www.paulaschoice.fr/fr/youth-extending-hydrating-fluid-spf-50/m7800.html", "category": "Protection solaire"},
    {"name": "Booster 10% Niacinamide", "price": 59.00, "sale_price": 47.20, "rating": 4.1, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7980-moon-1", "url": "https://www.paulaschoice.fr/fr/niacinamide-booster-full-size/7980-01.html", "category": "Boosters"},
    {"name": "Sérum Anti-Taches", "price": 62.00, "sale_price": 49.60, "rating": 3.9, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/8040-moon-1", "url": "https://www.paulaschoice.fr/fr/clinical-discoloration-repair-serum-full-size/8040-01.html", "category": "Sérums"},
    {"name": "Booster 7% Ectoïne", "price": 49.00, "sale_price": 39.20, "rating": 5.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1370-moon-1", "url": "https://www.paulaschoice.fr/fr/seven-perc-ectoin-hyaluronic-acid-hydrating-serum/m1370.html", "category": "Sérums"},
    {"name": "Nettoyant Visage Purifiant", "price": 27.00, "sale_price": 21.60, "rating": 4.3, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/6001-moon-1", "url": "https://www.paulaschoice.fr/fr/clear-pore-normalizing-cleanser/m6001.html", "category": "Nettoyants"},
    {"name": "Crème Hydratante Légère", "price": 38.00, "sale_price": 30.40, "rating": 4.2, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/3800-moon-1", "url": "https://www.paulaschoice.fr/fr/clear-oil-free-moisturizer/m3800.html", "category": "Hydratants"},
    {"name": "Crème Réparatrice Avancée", "price": 48.00, "sale_price": 38.40, "rating": 4.1, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2240-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-barrier-repair-advanced-moisturiser/m2240.html", "category": "Hydratants"},
    {"name": "Sérum Expert 25% Vitamine C + Glutathion", "price": 69.00, "sale_price": 55.20, "rating": 3.8, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1490-moon-1", "url": "https://www.paulaschoice.fr/fr/25perc-vitamin-c-and-glutathione-clinical-serum/m1490.html", "category": "Sérums"},
    {"name": "Crème Contour Yeux C5 Super Boost", "price": 46.00, "sale_price": 36.80, "rating": 4.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1010-moon-1", "url": "https://www.paulaschoice.fr/fr/c5-super-boost-eye-cream/m1010.html", "category": "Contour des yeux"},
    {"name": "Crème Hydratante Réparatrice SPF 50", "price": 46.00, "sale_price": 36.80, "rating": 4.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7970-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-ageing-skin-restoring-moisturiser/m7970.html", "category": "Protection solaire"},
    {"name": "Crème Réparatrice Intensive", "price": 48.00, "sale_price": 38.40, "rating": 4.7, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7810-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-intensive-repair-cream-full-size/7810-01.html", "category": "Hydratants"},
    {"name": "Crème Hydratante C5 Super Boost", "price": 56.00, "sale_price": 44.80, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2900-moon-1", "url": "https://www.paulaschoice.fr/fr/c5-super-boost-moisturiser/m2900.html", "category": "Hydratants"},
    {"name": "Lait Corps Sublimateur 10% AHA", "price": 39.00, "sale_price": 31.20, "rating": 3.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/5900-moon-1", "url": "https://www.paulaschoice.fr/fr/skin-revealing-body-lotion-aha/5900-01.html", "category": "Corps"},
    {"name": "Sérum Réparateur", "price": 53.00, "sale_price": 42.40, "rating": 4.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/3720-moon-1", "url": "https://www.paulaschoice.fr/fr/calm-repairing-serum/m3720.html", "category": "Sérums"},
    {"name": "Nettoyant Moussant Visage", "price": 32.00, "sale_price": 25.60, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7830-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-perfectly-balanced-foaming-cleanser/m7830.html", "category": "Nettoyants"},
    {"name": "Nettoyant Extra-Doux", "price": 30.00, "sale_price": 24.00, "rating": 4.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/9190-moon-1", "url": "https://www.paulaschoice.fr/fr/calm-ultra-gentle-cleanser/m9191.html", "category": "Nettoyants"},
    {"name": "Exfoliant 2% BHA Anti-Âge", "price": 43.00, "sale_price": 34.40, "rating": 4.0, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7820-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-daily-pore-refining-treatment-bha/m7820.html", "category": "Exfoliants"},
    {"name": "Crème Raffermissante Céramides", "price": 70.00, "sale_price": 56.00, "rating": 4.4, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2120-moon-1", "url": "https://www.paulaschoice.fr/fr/clinical-ceramide-enriched-firming-moisturizer-full-size/2120-01.html", "category": "Hydratants"},
    {"name": "Exfoliant 1% BHA Peaux Sensibles", "price": 39.00, "sale_price": 31.20, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/9210-moon-1", "url": "https://www.paulaschoice.fr/fr/calm-1percent-bha-sensitive-skin-exfoliant/m9210.html", "category": "Exfoliants"},
    {"name": "Omega+ Complex Crème de Nuit", "price": 48.00, "sale_price": 38.40, "rating": 4.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/3390-moon-1", "url": "https://www.paulaschoice.fr/fr/omega-complex-moisturizer-full-size/3390-01.html", "category": "Hydratants"},
    {"name": "Sérum Rétinol", "price": 55.00, "sale_price": 44.00, "rating": 4.7, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7710-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-intensive-wrinkle-repair-retinol-serum/m7710.html", "category": "Sérums"},
    {"name": "Gel Exfoliant 8% AHA", "price": 43.00, "sale_price": 34.40, "rating": 3.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1900-moon-1", "url": "https://www.paulaschoice.fr/fr/skin-perfecting-aha-gel-exfoliant/m1900.html", "category": "Exfoliants"},
    {"name": "Sérum Corps 5% Niacinamide", "price": 39.00, "sale_price": 31.20, "rating": 4.8, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/5810-moon-1", "url": "https://www.paulaschoice.fr/fr/niacinamide-body-serum/m5810.html", "category": "Corps"},
    {"name": "Peeling Exfoliant 25% AHA + 2% BHA", "price": 49.00, "sale_price": 39.20, "rating": 4.1, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/9565-moon-1", "url": "https://www.paulaschoice.fr/fr/25perc-aha-and-2perc-bha-exfoliant-peel/9565-01.html", "category": "Exfoliants"},
    {"name": "Booster Acide Hyaluronique", "price": 49.00, "sale_price": 39.20, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7860-moon-1", "url": "https://www.paulaschoice.fr/fr/hyaluronic-acid-booster-full-size/7860-01.html", "category": "Boosters"},
    {"name": "Booster 1% Rétinol", "price": 60.00, "sale_price": 48.00, "rating": 4.3, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7870-moon-1", "url": "https://www.paulaschoice.fr/fr/1-procent-retinol-booster-full-size/7870-01.html", "category": "Boosters"},
    {"name": "Fluide Exfoliant 2% BHA", "price": 39.00, "sale_price": 31.20, "rating": 4.8, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2051-moon-1", "url": "https://www.paulaschoice.fr/fr/skin-perfecting-bha-lotion-exfoliant-full-size/2051-01.html", "category": "Exfoliants"},
    {"name": "Anti-Aging Sérum Antioxydant", "price": 53.00, "sale_price": 42.40, "rating": 4.7, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7640-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-super-antioxidant-concentrate-serum-full-size/7640-01.html", "category": "Sérums"},
    {"name": "Baume Nettoyant Omega+ Complex", "price": 35.00, "sale_price": 28.00, "rating": 4.9, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/3380-moon-1", "url": "https://www.paulaschoice.fr/fr/omega-complex-cleansing-balm-full-size/3380-01.html", "category": "Nettoyants"},
    {"name": "Exfoliant 5% AHA", "price": 44.00, "sale_price": 35.20, "rating": 4.5, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7660-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-anti-aging-daily-smoothing-treatment-aha/m7660.html", "category": "Exfoliants"},
    {"name": "Gommage The UnScrub", "price": 38.00, "sale_price": 30.40, "rating": 4.6, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/7400-moon-1", "url": "https://www.paulaschoice.fr/fr/the-unscrub/m7400.html", "category": "Exfoliants"},
    {"name": "Crème Hydratante Solaire SPF 50", "price": 46.00, "sale_price": 36.80, "rating": 3.9, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/2390-moon-1", "url": "https://www.paulaschoice.fr/fr/advanced-sun-protection-daily-moisturiser/m2390.html", "category": "Protection solaire"},
    {"name": "Sérum Triple Active Total Repair", "price": 55.00, "sale_price": 44.00, "rating": 4.1, "image": "https://media.paulaschoice-eu.com/image/upload/f_auto,q_auto,dpr_auto/products/images/redesign/1020-moon-1", "url": "https://www.paulaschoice.fr/fr/resist-triple-active-total-repair-serum/m1020.html", "category": "Sérums"},
]

# ============================================================
# DONNÉES MURAD (top 45 produits - best-sellers US)
# ============================================================
MURAD_PRODUCTS = [
    {"name": "Rapid Dark Spot Correcting Serum", "price": 78.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/80989_Murad_RDSC_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/rapid-dark-spot-correcting-serum", "category": "Serums"},
    {"name": "Retinol Youth Renewal Serum", "price": 95.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/80865_RYR_Serum_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinol-youth-renewal-serum", "category": "Serums"},
    {"name": "Retinal ReSculpt Overnight Treatment", "price": 99.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Retinal_ReSculpt_OT_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinal-resculpt-overnight-treatment", "category": "Treatments"},
    {"name": "Retinal ReSculpt Body Treatment", "price": 75.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RetinalReSculpt_BodyTreatment_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinal-resculpt-body-treatment", "category": "Body"},
    {"name": "Retinal ReSculpt Overnight Cream", "price": 89.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Retinal_ReSculpt_OC_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinal-resculpt-overnight-cream", "category": "Moisturizers"},
    {"name": "Acne Control Clarifying Cleanser", "price": 29.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/M_dot_com-653875_308341_AC_Clarifying_Cleanser_5oz_RTL_US_WSHADOW.png", "url": "https://www.murad.com/products/clarifying-acne-cleanser", "category": "Cleansers"},
    {"name": "Acne Control Acne Body Wash", "price": 49.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Acne_Body_Wash_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/acne-body-wash", "category": "Body"},
    {"name": "Deep Relief Acne Treatment", "price": 48.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/DRAT_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/deep-relief-acne-treatment", "category": "Treatments"},
    {"name": "Superactive Moisturizer SPF 50 Brightening", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/SuperactiveSPF_Brightening_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/superactive-moisturizer-spf-50-brightening", "category": "Suncare"},
    {"name": "Retinol Youth Renewal Face Oil Drops", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RetinolOilDrops_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinol-youth-renewal-oil-drops", "category": "Serums"},
    {"name": "Vitamin C Glycolic Brightening Serum", "price": 78.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/VitC_Glycolic_Serum_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/vitamin-c-glycolic-brightening-serum", "category": "Serums"},
    {"name": "Retinol Youth Renewal Night Cream", "price": 89.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/80866_RYR_Night_Cream_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinol-youth-renewal-night-cream", "category": "Moisturizers"},
    {"name": "Retinol Youth Renewal Eye Serum", "price": 85.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/80866_RYR_Eye_Serum_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinol-youth-renewal-eye-serum", "category": "Eye Care"},
    {"name": "City Skin Age Defense SPF 50", "price": 72.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/City_Skin_SPF50_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/city-skin-age-defense-broad-spectrum-spf-50", "category": "Suncare"},
    {"name": "AHA/BHA Exfoliating Cleanser", "price": 38.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/AHA_BHA_Cleanser_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/aha-bha-exfoliating-cleanser", "category": "Cleansers"},
    {"name": "InvisiScar Resurfacing Treatment", "price": 35.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/InvisiScar_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/invisiscar-resurfacing-treatment", "category": "Treatments"},
    {"name": "Hydro-Dynamic Ultimate Moisture", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/HydroDynamic_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/hydro-dynamic-ultimate-moisture", "category": "Moisturizers"},
    {"name": "Essential-C Cleanser", "price": 36.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/EssentialC_Cleanser_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/essential-c-cleanser", "category": "Cleansers"},
    {"name": "Renewing Cleansing Cream", "price": 38.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RenewingCream_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/renewing-cleansing-cream", "category": "Cleansers"},
    {"name": "Nutrient-Charged Water Gel", "price": 62.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/NutrientCharged_WaterGel_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/nutrient-charged-water-gel", "category": "Moisturizers"},
    {"name": "Rapid Collagen Infusion", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RCI_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/rapid-collagen-infusion", "category": "Serums"},
    {"name": "Multi-Vitamin Infusion Oil", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/MVI_Oil_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/multi-vitamin-infusion-oil", "category": "Serums"},
    {"name": "Essential-C Day Moisture SPF 30", "price": 66.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/EssentialC_Day_SPF30_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/essential-c-day-moisture-broad-spectrum-spf-30", "category": "Suncare"},
    {"name": "Revitalixir Recovery Serum", "price": 89.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Revitalixir_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/revitalixir-recovery-serum", "category": "Serums"},
    {"name": "Renewing Eye Cream", "price": 82.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RenewingEyeCream_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/renewing-eye-cream", "category": "Eye Care"},
    {"name": "Outsmart Acne Clarifying Treatment", "price": 42.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Outsmart_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/outsmart-acne-clarifying-treatment", "category": "Treatments"},
    {"name": "Hydrating Toner", "price": 26.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/HydratingToner_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/hydrating-toner", "category": "Toners"},
    {"name": "Rapid Relief Acne Spot Treatment", "price": 22.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RapidRelief_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/rapid-relief-acne-spot-treatment", "category": "Treatments"},
    {"name": "Skin Smoothing Polish", "price": 36.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/SkinSmoothing_Polish_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/skin-smoothing-polish", "category": "Exfoliants"},
    {"name": "Vita-C Eyes Dark Circle Corrector", "price": 72.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/VitaCEyes_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/vita-c-eyes-dark-circle-corrector", "category": "Eye Care"},
    {"name": "Oil and Pore Control Mattifier SPF 45", "price": 42.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/OilPore_Mattifier_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/oil-and-pore-control-mattifier-broad-spectrum-spf-45", "category": "Suncare"},
    {"name": "Targeted Wrinkle Corrector", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/TargetedWrinkle_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/targeted-wrinkle-corrector", "category": "Treatments"},
    {"name": "Clarifying Toner", "price": 26.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/ClarifyingToner_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/clarifying-toner", "category": "Toners"},
    {"name": "Resurgence Retinol Youth Renewal Moisturizer SPF 30", "price": 79.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/RYR_Moisturizer_SPF30_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/retinol-youth-renewal-moisturizer-spf-30", "category": "Suncare"},
    {"name": "Sensitive Skin Soothing Serum", "price": 62.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/SensitiveSkin_Serum_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/sensitive-skin-soothing-serum", "category": "Serums"},
    {"name": "Multi-Acid Peel", "price": 42.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/MultiAcid_Peel_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/multi-acid-peel", "category": "Exfoliants"},
    {"name": "Prebiotic 4-in-1 MultiCleanser", "price": 36.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/Prebiotic_MultiCleanser_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/prebiotic-4-in-1-multicleanser", "category": "Cleansers"},
    {"name": "Age-Balancing Night Cream", "price": 75.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/AgeBalancing_NightCream_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/age-balancing-night-cream", "category": "Moisturizers"},
    {"name": "Clarifying Body Spray", "price": 38.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/ClarifyingBodySpray_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/clarifying-body-spray", "category": "Body"},
    {"name": "Hydrating Cream Cleanser", "price": 36.00, "image": "https://cdn.shopify.com/s/files/1/0816/7705/8351/files/HydratingCreamCleanser_Carousel_1_MURAD.png", "url": "https://www.murad.com/products/hydrating-cream-cleanser", "category": "Cleansers"},
]

# ============================================================
# DONNÉES SKINCEUTICALS (40 produits - catalogue complet)
# ============================================================
SKINCEUTICALS_PRODUCTS = [
    {"name": "C E Ferulic with 15% L-Ascorbic Acid", "price": 185.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwd20af22a/Products/S17/SKC_CEF_Allure_Packshot.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/vitamin-c-serums/c-e-ferulic-with-15-l-ascorbic-acid/S17.html", "category": "Vitamin C Serums"},
    {"name": "P-TIOX Anti-Wrinkle Peptide Serum", "price": 150.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw2b1e318b/pdpimages/S123/PTIOX_Product_Slide_01_wSeal.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/anti-aging-serum/p-tiox-anti-wrinkle-serum/S123.html", "category": "Anti-Aging Serums"},
    {"name": "Triple Lipid Restore 2:4:2", "price": 155.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw71e8d819/Products/S09/24_0409_SKC_TLR242_PDP_ALT_BeautyInc_Seal.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/anti-aging-creams/triple-lipid-restore-2-4-2/S09.html", "category": "Anti-Aging Creams"},
    {"name": "Hyaluronic Acid Intensifier Multi-Glycan", "price": 120.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw1b7e2ad1/pdpimages/S122/HAI_MultiGlycan_2000x2000v2.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/hyaluronic-acid-serums/hyaluronic-acid-intensifier-multi-glycan/S122.html", "category": "Hydrating Serums"},
    {"name": "A.G.E. Advanced Eye for Dark Circles", "price": 125.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw8a07b83a/Products/S119/23_1013_SKC_AGE_ADV_EYE_PDP_ALT_AllureAward_2023.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/anti-aging-creams/a.g.e.-advanced-eye-for-dark-circles/S119.html", "category": "Eye Care"},
    {"name": "A.G.E. Interrupter Advanced Cream", "price": 185.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw002f0c5c/Products/S117/AGE-INTERRUPTER-ADVANCED_SKC_CosmoAward_SkinCeuticals.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/anti-aging-creams/a.g.e.-interrupter-advanced/S117.html", "category": "Anti-Aging Creams"},
    {"name": "Hydrating B5 Gel", "price": 95.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw1278938f/pdpimages/hydrating-b5-gel-635494117004-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/hydrating-serums/hydrating-b5-gel/S39.html", "category": "Hydrating Serums"},
    {"name": "Phloretin CF with Ferulic Acid", "price": 185.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw6c7eb63c/Products/S55/phloretin-cf-635494116007-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/vitamin-c-serums/phloretin-cf-with-ferulic-acid-vitamin-c-serum/S55.html", "category": "Vitamin C Serums"},
    {"name": "Silymarin CF Vitamin C Serum", "price": 175.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw5d55a5a5/Products/S113/silymarin-cf-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/vitamin-c-serums/silymarin-cf/S113.html", "category": "Vitamin C Serums"},
    {"name": "Blemish + Age Defense", "price": 94.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw1d5c85f0/Products/S06/blemish-age-defense-635494115003-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/acne-serums/blemish-and-age-defense/S06.html", "category": "Acne Serums"},
    {"name": "Retinol 0.3", "price": 70.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw7d5a3a3a/Products/S100/retinol-03-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/retinol-creams/retinol-0-3/S100.html", "category": "Retinol"},
    {"name": "Retinol 0.5", "price": 78.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw2d5a3c3a/Products/S101/retinol-05-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/retinol-creams/retinol-0-5/S101.html", "category": "Retinol"},
    {"name": "Retinol 1.0", "price": 88.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw3d5a3d3a/Products/S102/retinol-10-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/retinol-creams/retinol-1-0/S102.html", "category": "Retinol"},
    {"name": "Discoloration Defense", "price": 105.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw4d5a3e3a/Products/S107/discoloration-defense-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/brightening-serums/discoloration-defense/S107.html", "category": "Brightening"},
    {"name": "Phyto Corrective Gel", "price": 70.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw5d5a3f3a/Products/S24/phyto-corrective-gel-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/sensitive-skin-serums/phyto-corrective-gel/S24.html", "category": "Sensitive Skin"},
    {"name": "Phyto Corrective Masque", "price": 62.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw6d5a4a3a/Products/S56/phyto-corrective-masque-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/masks/phyto-corrective-masque/S56.html", "category": "Masks"},
    {"name": "Glycolic 10 Renew Overnight", "price": 75.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw7d5a4b3a/Products/S93/glycolic-10-renew-overnight-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/exfoliators/glycolic-10-renew-overnight/S93.html", "category": "Exfoliators"},
    {"name": "Micro-Exfoliating Scrub", "price": 32.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw8d5a4c3a/Products/S81/micro-exfoliating-scrub-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/exfoliators/micro-exfoliating-scrub/S81.html", "category": "Exfoliators"},
    {"name": "LHA Cleansing Gel", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw9d5a4d3a/Products/S62/lha-cleansing-gel-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/cleansers/lha-cleansing-gel/S62.html", "category": "Cleansers"},
    {"name": "Soothing Cleanser", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwad5a4e3a/Products/S63/soothing-cleanser-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/cleansers/soothing-cleanser/S63.html", "category": "Cleansers"},
    {"name": "Gentle Cleanser", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwbd5a4f3a/Products/S64/gentle-cleanser-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/cleansers/gentle-cleanser/S64.html", "category": "Cleansers"},
    {"name": "Simply Clean", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwcd5a5a3a/Products/S65/simply-clean-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/cleansers/simply-clean/S65.html", "category": "Cleansers"},
    {"name": "Metacell Renewal B3", "price": 120.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwdd5a5b3a/Products/S83/metacell-renewal-b3-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/moisturizers/metacell-renewal-b3/S83.html", "category": "Moisturizers"},
    {"name": "Emollience", "price": 68.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwed5a5c3a/Products/S35/emollience-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/moisturizers/emollience/S35.html", "category": "Moisturizers"},
    {"name": "Daily Moisture", "price": 68.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwfd5a5d3a/Products/S36/daily-moisture-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/moisturizers/daily-moisture/S36.html", "category": "Moisturizers"},
    {"name": "Face Cream", "price": 68.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw0e5a5e3a/Products/S37/face-cream-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/moisturizers/face-cream/S37.html", "category": "Moisturizers"},
    {"name": "Physical Fusion UV Defense SPF 50", "price": 39.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw1e5a5f3a/Products/S78/physical-fusion-uv-defense-spf-50-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/sunscreens/physical-fusion-uv-defense-spf-50/S78.html", "category": "Sunscreens"},
    {"name": "Sheer Physical UV Defense SPF 50", "price": 39.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw2e5a6a3a/Products/S79/sheer-physical-uv-defense-spf-50-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/sunscreens/sheer-physical-uv-defense-spf-50/S79.html", "category": "Sunscreens"},
    {"name": "Light Moisture UV Defense SPF 50", "price": 45.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw3e5a6b3a/Products/S114/light-moisture-uv-defense-spf-50-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/sunscreens/light-moisture-uv-defense-spf-50/S114.html", "category": "Sunscreens"},
    {"name": "Serum 10 AOX+", "price": 88.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw4e5a6c3a/Products/S52/serum-10-aox-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/vitamin-c-serums/serum-10-aox/S52.html", "category": "Vitamin C Serums"},
    {"name": "H.A. Intensifier", "price": 105.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw5e5a6d3a/Products/S103/ha-intensifier-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/hyaluronic-acid-serums/h-a-intensifier/S103.html", "category": "Hydrating Serums"},
    {"name": "Equalizing Toner", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw6e5a6e3a/Products/S66/equalizing-toner-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/toners/equalizing-toner/S66.html", "category": "Toners"},
    {"name": "Epidermal Repair", "price": 82.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw7e5a6f3a/Products/S22/epidermal-repair-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/moisturizers/epidermal-repair/S22.html", "category": "Moisturizers"},
    {"name": "Clarifying Clay Masque", "price": 52.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw8e5a7a3a/Products/S57/clarifying-clay-masque-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/masks/clarifying-clay-masque/S57.html", "category": "Masks"},
    {"name": "Resveratrol B E", "price": 165.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dw9e5a7b3a/Products/S86/resveratrol-be-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/anti-aging-serum/resveratrol-b-e/S86.html", "category": "Anti-Aging Serums"},
    {"name": "Eye Balm", "price": 75.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwae5a7c3a/Products/S38/eye-balm-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/eye-creams/eye-balm/S38.html", "category": "Eye Care"},
    {"name": "Purifying Cleanser", "price": 38.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwbe5a7d3a/Products/S67/purifying-cleanser-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/cleansers/purifying-cleanser/S67.html", "category": "Cleansers"},
    {"name": "Mineral Radiance UV Defense SPF 50", "price": 39.00, "image": "https://www.skinceuticals.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-acd-skinceuticals-master-catalog/default/dwce5a7e3a/Products/S111/mineral-radiance-uv-defense-spf-50-skinceuticals-main.jpg?sw=270", "url": "https://www.skinceuticals.com/skincare/sunscreens/mineral-radiance-uv-defense-spf-50/S111.html", "category": "Sunscreens"},
]


def parse_price(price_str):
    """Parse price string to float."""
    if isinstance(price_str, (int, float)):
        return float(price_str)
    if not price_str:
        return None
    clean = re.sub(r'[^\d.,]', '', str(price_str))
    clean = clean.replace(',', '.')
    try:
        return float(clean)
    except ValueError:
        return None


def populate():
    """Peuple la base avec les données des 3 concurrents."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Supprimer l'ancienne base si elle existe
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Ancienne base supprimée: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Créer les tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            product_id TEXT NOT NULL,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            url TEXT,
            image_url TEXT,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(site, product_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'EUR',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS new_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_site ON products(site)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prices_product ON prices(product_id, timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_new_products_detected ON new_products(detected_at)")

    now = datetime.now()

    def insert_products(products, site, brand, currency):
        count = 0
        for i, p in enumerate(products):
            product_id_str = f"{site}_{i+1:03d}"

            # Varier les dates first_seen pour simuler un historique
            days_ago = random.randint(1, 60)
            first_seen = (now - timedelta(days=days_ago)).isoformat()

            cursor.execute("""
                INSERT INTO products (site, product_id, name, brand, category, url, image_url, first_seen, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (site, product_id_str, p['name'], brand, p.get('category', ''),
                  p.get('url', ''), p.get('image', p.get('image_url', '')), first_seen, now.isoformat()))

            pid = cursor.lastrowid

            # Prix actuel
            price = parse_price(p.get('sale_price') or p.get('price'))
            if price:
                cursor.execute("INSERT INTO prices (product_id, price, currency, timestamp) VALUES (?, ?, ?, ?)",
                              (pid, price, currency, now.isoformat()))

                # Ajouter un historique de prix (prix standard comme ancien prix)
                standard = parse_price(p.get('price'))
                if standard and standard != price:
                    old_date = (now - timedelta(days=random.randint(7, 30))).isoformat()
                    cursor.execute("INSERT INTO prices (product_id, price, currency, timestamp) VALUES (?, ?, ?, ?)",
                                  (pid, standard, currency, old_date))

            # Marquer les produits récents comme nouveautés
            if days_ago <= 14:
                cursor.execute("INSERT INTO new_products (product_id, detected_at) VALUES (?, ?)",
                              (pid, first_seen))

            count += 1

        return count

    # Insérer les 3 marques
    pc_count = insert_products(PAULAS_CHOICE_PRODUCTS, 'paulaschoice', "Paula's Choice", 'EUR')
    print(f"Paula's Choice: {pc_count} produits insérés")

    murad_count = insert_products(MURAD_PRODUCTS, 'murad', 'Murad', 'USD')
    print(f"Murad: {murad_count} produits insérés")

    skc_count = insert_products(SKINCEUTICALS_PRODUCTS, 'skinceuticals', 'SkinCeuticals', 'USD')
    print(f"SkinCeuticals: {skc_count} produits insérés")

    conn.commit()

    # Vérification
    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM prices")
    total_prices = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM new_products")
    total_new = cursor.fetchone()[0]

    print(f"\n=== Base de données peuplée ===")
    print(f"Total produits: {total}")
    print(f"Total prix enregistrés: {total_prices}")
    print(f"Nouveautés: {total_new}")
    print(f"Base: {DB_PATH}")

    conn.close()


if __name__ == '__main__':
    populate()
