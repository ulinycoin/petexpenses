import os
import csv
import re

# Data extracted from index.html
DOG_BREEDS = {
    'Cavalier King Charles Spaniel':['small','long',1.5,1.5,1,1.2,'High cardiac & neurological risk'],
    'Pug':['small','short',1.6,1.6,1,.9,'Brachycephalic syndrome'],
    'French Bulldog':['small','short',1.7,1.7,1,.9,'Breathing & spine issues'],
    'Boston Terrier':['small','short',1.4,1.4,1,.9,'Eye & joint issues'],
    'Miniature Schnauzer':['small','wire',1.15,1.15,1,1.3,'Pancreatitis & bladder stones'],
    'Jack Russell Terrier':['small','short',1.1,1.1,1,1,'Very healthy; high energy'],
    'Beagle':['small','short',1.2,1.2,1.1,1,'Obesity & epilepsy risk'],
    'Cocker Spaniel':['medium','long',1.25,1.25,1,1.4,'Ear & eye issues'],
    'Miniature Poodle':['small','wire',1.1,1.1,1,1.4,'Healthy; needs grooming'],
    'Havanese':['small','long',1.1,1.1,.95,1.3,'Joint & eye issues'],
    'Papillon':['small','long',1.05,1.05,.9,1.1,'Long-lived, healthy'],
    'Bichon Frise':['small','wire',1.15,1.15,.95,1.4,'Skin allergies; needs grooming'],
    'Italian Greyhound':['small','short',1.15,1.15,.9,.8,'Fragile bones; dental'],
    'Lhasa Apso':['small','long',1.15,1.15,.95,1.4,'Kidney & eye issues'],
    'Rat Terrier':['small','short',1,1,.95,.8,'Very hardy'],
    'Cockapoo':['small','wire',1.1,1.1,.95,1.4,'Ear infections; grooming'],
    'Cavapoo':['small','wire',1.15,1.15,.95,1.4,'Possible MVD heart risk'],
    'Labrador Retriever':['large','short',1.2,1.2,1.1,1,'Hip dysplasia & obesity risk'],
    'Golden Retriever':['large','long',1.25,1.3,1.1,1.2,'High cancer risk'],
    'German Shepherd':['large','long',1.3,1.3,1.1,1.1,'Hip dysplasia common'],
    'Bulldog':['medium','short',1.8,1.8,1,.9,'Very high lifetime vet costs'],
    'Poodle':['medium','wire',1.1,1.1,1,1.5,"Addison's disease risk"],
    'Boxer':['large','short',1.4,1.4,1.1,.9,'Heart issues & cancer rate'],
    'Siberian Husky':['medium','long',1.1,1.1,1.2,1.2,'Eye & hip issues'],
    'Australian Shepherd':['medium','long',1.15,1.15,1.1,1.2,'MDR1 mutation; epilepsy'],
    'Border Collie':['medium','long',1.1,1.1,1.1,1.2,'Epilepsy & CEA risk'],
    'Shiba Inu':['medium','long',1.1,1.1,1,1.1,'Allergies & hip risk'],
    'Corgi (Pembroke)':['small','long',1.2,1.2,1.05,1.1,'Back & hip; obesity'],
    'Whippet':['medium','short',1.05,1.05,1,.8,'Very healthy'],
    'Vizsla':['medium','short',1.1,1.1,1.1,.8,'Epilepsy & hip risk'],
    'Weimaraner':['large','short',1.2,1.2,1.1,.9,'Bloat & hip risk'],
    'Samoyed':['medium','long',1.2,1.2,1.1,1.5,'Diabetes & heart issues'],
    'Chow Chow':['medium','long',1.3,1.3,1,1.4,'Hip & eye issues'],
    'Akita':['large','long',1.25,1.25,1.1,1.1,'Autoimmune & kidney'],
    'Rottweiler':['large','short',1.35,1.35,1.1,.9,'Hip & high cancer rate'],
    'Doberman Pinscher':['large','short',1.3,1.3,1.1,.9,'Cardiomyopathy risk'],
    'Bernese Mountain Dog':['large','long',1.5,1.6,1.1,1.3,'Short lifespan ~7–8 yrs'],
    'Dalmatian':['medium','short',1.2,1.2,1,.9,'Deafness & urinary stones'],
    'Bernedoodle':['large','wire',1.2,1.25,1.1,1.5,'High grooming needs'],
    'Great Dane':['giant','short',1.4,1.5,1.1,.9,'Bloat; lifespan 7–10 yrs'],
    'Saint Bernard':['giant','long',1.3,1.4,1.2,1.2,'Hip & heart issues'],
    'Mastiff':['giant','short',1.3,1.4,1.15,.9,'Hip dysplasia; bloat'],
    'Newfoundland':['giant','long',1.3,1.35,1.2,1.3,'Heart disease (SAS)'],
    'Standard Poodle':['large','wire',1.1,1.1,1.05,1.5,"Addison's; bloat risk"],
    'Cane Corso':['giant','short',1.2,1.3,1.15,.9,'Hip; cherry eye risk']
}

CAT_BREEDS = {
    'Domestic Shorthair':['medium','short',1,1,1,.8,'The classic — generally healthy'],
    'Domestic Longhair':['medium','long',1.05,1.05,1,1.3,'Brushing 2–3× per week'],
    'Maine Coon':['large','long',1.25,1.3,1.2,1.4,'HCM heart condition risk'],
    'Ragdoll':['large','long',1.2,1.25,1.1,1.3,'HCM & UTI risk; very affectionate'],
    'Persian':['medium','long',1.4,1.4,1,1.6,'Brachycephalic; daily grooming'],
    'Siamese':['medium','short',1.15,1.15,1,.8,'Dental & respiratory issues'],
    'British Shorthair':['medium','short',1.15,1.2,1,.9,'HCM risk; placid'],
    'Bengal':['medium','short',1.15,1.15,1.1,.9,'High energy; HCM risk'],
    'Sphynx':['medium','short',1.4,1.4,1.05,1.2,'Skin care + weekly bathing'],
    'Scottish Fold':['medium','short',1.5,1.5,1,1,'Osteochondrodysplasia (joint pain)'],
    'Russian Blue':['medium','short',1,1,1,.9,'Very healthy, low-maintenance'],
    'Abyssinian':['medium','short',1.15,1.15,1,.8,'Renal amyloidosis risk'],
    'Norwegian Forest Cat':['large','long',1.2,1.2,1.15,1.4,'HCM & hip dysplasia'],
    'American Shorthair':['medium','short',1.05,1.05,1,.8,'Generally hardy'],
    'Exotic Shorthair':['medium','short',1.35,1.35,1,1,'Brachycephalic like Persian'],
    'Burmese':['medium','short',1.2,1.2,1,.8,'Diabetes & cranial issues'],
    'Birman':['medium','long',1.1,1.1,1,1.2,'Generally healthy'],
    'Oriental Shorthair':['medium','short',1.1,1.1,1,.8,'Dental & cardiac risk'],
    'Devon Rex':['small','short',1.15,1.15,.95,.9,'Patellar luxation'],
    'Cornish Rex':['small','short',1.15,1.15,.95,.9,'HCM & hypotrichosis'],
    'Savannah':['large','short',1.2,1.25,1.2,.9,'High energy; pricey vet'],
    'Manx':['medium','short',1.3,1.3,1,.9,'Manx syndrome (spine)'],
    'Tonkinese':['medium','short',1.1,1.1,1,.8,'Generally healthy']
}

DOG_COSTS = {
    'food': {'small': [360,600], 'medium': [600,1000], 'large': [900,1500], 'giant': [1200,2000]},
    'vet': {'small': [200,500], 'medium': [300,700], 'large': [400,1000], 'giant': [500,1200]},
    'insurance': {'small': [240,480], 'medium': [360,720], 'large': [480,960], 'giant': [600,1200]},
    'grooming': {
        'short': {'small': [100,200], 'medium': [150,300], 'large': [200,400], 'giant': [250,500]},
        'long': {'small': [200,400], 'medium': [300,500], 'large': [400,800], 'giant': [500,1000]},
        'wire': {'small': [180,350], 'medium': [250,450], 'large': [350,700], 'giant': [450,900]},
    },
    'supplies': {'small': [150,300], 'medium': [200,400], 'large': [250,500], 'giant': [300,600]},
}

CAT_COSTS = {
    'food': {'small': [240,420], 'medium': [300,600], 'large': [420,720]},
    'vet': {'small': [180,400], 'medium': [220,500], 'large': [300,650]},
    'insurance': {'small': [180,360], 'medium': [240,480], 'large': [300,540]},
    'grooming': {
        'short': {'small': [40,120], 'medium': [60,150], 'large': [80,180]},
        'long': {'small': [120,300], 'medium': [180,400], 'large': [240,500]},
    },
    'supplies': {'small': [120,240], 'medium': [150,300], 'large': [200,380]},
}

def make_slug(name):
    slug = name.lower()
    slug = slug.replace(' (pembroke)', '-pembroke')
    slug = slug.replace("'", '')
    slug = slug.replace(' & ', '-and-')
    slug = re.sub(r'[^a-z0-9-]', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug + '-cost'

def calculate_costs(data, species):
    size = data[0]
    coat = data[1]
    multi_low = data[2]
    multi_high = data[3]
    
    costs = DOG_COSTS if species == 'dog' else CAT_COSTS
    
    food = costs['food'][size]
    vet = costs['vet'][size]
    ins = costs['insurance'][size]
    groom = costs['grooming'][coat][size]
    supp = costs['supplies'][size]
    
    cl = int((food[0] + vet[0] + ins[0] + groom[0] + supp[0]) * multi_low)
    ch = int((food[1] + vet[1] + ins[1] + groom[1] + supp[1]) * multi_high)
    return cl, ch

# Generate records
lines = []
for breed, data in DOG_BREEDS.items():
    cl, ch = calculate_costs(data, 'dog')
    slug = make_slug(breed)
    lines.append({
        'Breed': breed,
        'Species': 'Dog',
        'Annual Cost Range (US, 2026)': f"${cl:,}-${ch:,}/year",
        'URL': f"https://petexpenses.com/breeds/{slug}"
    })

for breed, data in CAT_BREEDS.items():
    cl, ch = calculate_costs(data, 'cat')
    slug = make_slug(breed)
    lines.append({
        'Breed': breed,
        'Species': 'Cat',
        'Annual Cost Range (US, 2026)': f"${cl:,}-${ch:,}/year",
        'URL': f"https://petexpenses.com/breeds/{slug}"
    })

# Write to CSV file
csv_path = "/Users/aleksejs/Desktop/dog-cost-tool/petexpenses-breed-costs-2026.csv"
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Breed', 'Species', 'Annual Cost Range (US, 2026)', 'URL'])
    writer.writeheader()
    writer.writerows(lines)

print(f"Successfully generated {len(lines)} breed cost ranges inside CSV!")
