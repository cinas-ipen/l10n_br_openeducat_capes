#!/usr/bin/env python3
"""
Procedural Synthetic Data Generator for l10n_br_openeducat_capes (Odoo 19.0)
Scenarios:
1. Universidade XYZQ (3 Academic Programs + 1 Professional Program with cohorts T1-T9)
2. MPTRCS / IPEN-CNEN/SP (Reference profile with external registration at USP)

Generates complete, non-repeating, realistic Brazilian academic datasets
with 100% of CAPES census fields (mother name, race/color, disability, birth city/state,
nationality, PIDs, degrees, work regimes) and distinct first_name, middle_name, last_name.
"""

import os
import csv
import random

RNG = random.Random(2026)

MALE_FIRST = [
    "Carlos", "Eduardo", "Lucas", "Fernando", "Guilherme", "Roberto", "Rodrigo", "Felipe",
    "Thiago", "Gabriel", "Alexandre", "André", "Bernardo", "Bruno", "César", "Daniel",
    "Danilo", "Diego", "Fábio", "Gustavo", "Henrique", "Igor", "João", "José", "Julio",
    "Leonardo", "Luiz", "Marcelo", "Marcio", "Marcos", "Mateus", "Maurício", "Murilo",
    "Nelson", "Otávio", "Paulo", "Pedro", "Rafael", "Renato", "Ricardo", "Samuel", "Sérgio",
    "Tiago", "Victor", "Vinícius"
]

FEMALE_FIRST = [
    "Mariana", "Juliana", "Camila", "Beatriz", "Larissa", "Renata", "Patricia", "Aline",
    "Leticia", "Vanessa", "Adriana", "Amanda", "Ana", "Bianca", "Bruna", "Carla", "Carolina",
    "Cecília", "Cláudia", "Cristina", "Daniela", "Débora", "Eduarda", "Elaine", "Fabiana",
    "Fernanda", "Flávia", "Gabriela", "Gisele", "Helena", "Isabela", "Isadora", "Jaqueline",
    "Jéssica", "Laura", "Lívia", "Luana", "Luciana", "Manuela", "Marina", "Natália", "Priscila",
    "Rachel", "Raquel", "Roberta", "Sabrina", "Tatiana", "Thais"
]

MIDDLES = [
    "Alves", "Barbosa", "Cardoso", "Carvalho", "Cavalcanti", "Correia", "Costa", "Dias",
    "Duarte", "Fernandes", "Ferreira", "Gomes", "Guimarães", "Lima", "Lopes", "Macedo",
    "Martins", "Melo", "Mendes", "Miranda", "Monteiro", "Moraes", "Moreira", "Nascimento",
    "Nogueira", "Oliveira", "Pereira", "Pinto", "Ramos", "Ribeiro", "Rocha", "Rodrigues",
    "Santana", "Santos", "Silva", "Silveira", "Soares", "Sousa", "Souza", "Teixeira", "Vieira"
]

LASTS = [
    "Alcantara", "Amaral", "Andrade", "Barcellos", "Barreto", "Bittencourt", "Botelho", "Bueno",
    "Caldeira", "Camargo", "Carneiro", "Chaves", "Cordeiro", "Dantas", "Delgado", "Drummond",
    "Esteves", "Fagundes", "Figueira", "Fontes", "Fragoso", "Galvao", "Guedes", "Junqueira",
    "Lacerda", "Leite", "Lemos", "Linhares", "Lobato", "Loyola", "Maciel", "Maia", "Malcher",
    "Marcondes", "Marinho", "Mascarenhas", "Matos", "Mello", "Meneses", "Mesquita", "Montenegro",
    "Morais", "Muniz", "Negrao", "Neves", "Nobrega", "Noronha", "Novais", "Padilha", "Penna",
    "Penteado", "Pimentel", "Pinheiro", "Pontes", "Portela", "Porto", "Quadros", "Rangel",
    "Resende", "Ribas", "Rolim", "Saldanha", "Salles", "Sampaio", "Sardenberg", "Seixas",
    "Serra", "Simas", "Sobral", "Tavora", "Torres", "Valadao", "Valenca", "Valle", "Vargas",
    "Vidal", "Villela", "Wanderley", "Zamboni"
]

MOTHER_FIRSTS = ["Maria", "Ana", "Regina", "Sônia", "Márcia", "Helena", "Lúcia", "Tereza", "Fátima", "Sandra", "Vera", "Denise"]
MOTHER_CONNECTORS = ["de Lourdes", "Aparecida", "Célia", "do Carmo", "das Graças", "Cristina", "Helena", "Beatriz"]
CITIES = [
    ("São Paulo", "SP"), ("Campinas", "SP"), ("Ribeirão Preto", "SP"), ("São José dos Campos", "SP"),
    ("Santos", "SP"), ("Sorocaba", "SP"), ("Belo Horizonte", "MG"), ("Curitiba", "PR"),
    ("Rio de Janeiro", "RJ"), ("Porto Alegre", "RS"), ("Salvador", "BA"), ("Recife", "PE")
]
STREETS = [
    "Av. Lineu Prestes", "Av. Paulista", "Rua da Consolação", "Rua Augusta", "Rua Vergueiro",
    "Av. Rebouças", "Rua Domingos de Morais", "Av. Angélica", "Rua Teodoro Sampaio", "Av. Faria Lima",
    "Rua Bela Cintra", "Av. Brigadeiro Luís Antônio"
]
RACES = ['white', 'white', 'brown', 'brown', 'black', 'yellow', 'indigenous']

USED_NAMES = set()

def gen_cpf(seed_int):
    local_rng = random.Random(seed_int)
    digits = [local_rng.randint(0, 9) for _ in range(9)]
    s1 = sum(digits[i] * (10 - i) for i in range(9))
    d1 = 11 - (s1 % 11)
    d1 = 0 if d1 >= 10 else d1
    digits.append(d1)
    s2 = sum(digits[i] * (11 - i) for i in range(10))
    d2 = 11 - (s2 % 11)
    d2 = 0 if d2 >= 10 else d2
    digits.append(d2)
    return ''.join(map(str, digits))

def gen_unique_identity(idx, gender_letter, domain="dominio.edu.br"):
    first_pool = MALE_FIRST if gender_letter == 'm' else FEMALE_FIRST
    first = first_pool[idx % len(first_pool)]
    
    attempts = 0
    while True:
        mid = MIDDLES[(idx * 7 + attempts * 13) % len(MIDDLES)]
        last = LASTS[(idx * 11 + attempts * 17) % len(LASTS)]
        full_name = f"{first} {mid} {last}"
        if full_name not in USED_NAMES:
            USED_NAMES.add(full_name)
            break
        attempts += 1
    
    cpf = gen_cpf(idx + 5000)
    m_first = MOTHER_FIRSTS[(idx * 3) % len(MOTHER_FIRSTS)]
    m_conn = MOTHER_CONNECTORS[(idx * 5) % len(MOTHER_CONNECTORS)]
    mother_name = f"{m_first} {m_conn} {last}"
    
    city, state_abbr = CITIES[idx % len(CITIES)]
    street = f"{STREETS[idx % len(STREETS)]}, {100 + (idx * 17) % 850}"
    street2 = f"Apto {(idx % 15) + 1}01" if idx % 2 == 0 else ""
    zip_code = f"0{1000 + (idx * 31) % 8900:04d}-{(idx * 19) % 890:03d}"
    phone = f"(11) 9{8000 + (idx * 23) % 1900:04d}-{(idx * 29) % 9000:04d}"
    race = RACES[idx % len(RACES)]
    has_disability = (idx % 25 == 0)
    email = f"{first.lower()}.{last.lower()}_{idx}@{domain}"
    
    return {
        'first_name': first,
        'middle_name': mid,
        'last_name': last,
        'full_name': full_name,
        'cpf': cpf,
        'email': email,
        'mother_name': mother_name,
        'city': city,
        'state_abbr': state_abbr,
        'street': street,
        'street2': street2,
        'zip': zip_code,
        'phone': phone,
        'race': race,
        'has_disability': has_disability,
        'gender': 'male' if gender_letter == 'm' else 'female',
    }

def write_csv(filepath, headers, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated: {filepath} ({len(rows)} records)")

# ------------------------------------------------------------------------------
# SCENARIO 1: UNIVERSIDADE XYZQ
# ------------------------------------------------------------------------------
def generate_scenario_xyzq(base_dir):
    print("--- Generating Scenario 1: Universidade XYZQ ---")
    out = os.path.join(base_dir, "universidade_xyzq")
    comp_id = "comp_ies_xyzq"
    
    # 01 Company
    write_csv(os.path.join(out, "01_ies_instituicao_res_company.csv"),
              ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
              [[comp_id, 'Universidade XYZQ', '12.345.678/0001-90', '12345', 'Av. Central Universitária, 1000', 'São Paulo', '01000-000', 'BR']])

    # 02 Programs
    progs = [
        ['prog_xyzq_cc', 'Programa de Pós-Graduação em Ciência da Computação', 'PPGCC', '33001010001P1', 'academic', '5', 'semestral', comp_id],
        ['prog_xyzq_fis', 'Programa de Pós-Graduação em Física Aplicada', 'PPGFA', '33001010002P8', 'academic', '6', 'semestral', comp_id],
        ['prog_xyzq_bio', 'Programa de Pós-Graduação em Biotecnologia Molecular', 'PPGBM', '33001010003P4', 'academic', '5', 'semestral', comp_id],
        ['prog_xyzq_mpe', 'Mestrado Profissional em Engenharia de Software e Inovação', 'MPESI', '33001010004P0', 'professional', '4', 'semestral', comp_id],
    ]
    write_csv(os.path.join(out, "02_programas_capes_op_program.csv"),
              ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id'], progs)

    # 03 Curriculum Versions
    regs = [
        ['reg_xyzq_cc_2024', 'Regimento PPGCC 2024', 'prog_xyzq_cc', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_fis_2024', 'Regimento PPGFA 2024', 'prog_xyzq_fis', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_bio_2024', 'Regimento PPGBM 2024', 'prog_xyzq_bio', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_mpe_2024', 'Regimento MPESI 2024', 'prog_xyzq_mpe', '100', '40', '52', '8', '15', '50', '24', 'False', '0', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'admission', 'not_applicable', 'cpg_checklist', 'hybrid_allowed'],
    ]
    write_csv(os.path.join(out, "03_versao_curricular_op_curriculum_version.csv"),
              ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'], regs)

    # 04 Áreas de Concentração
    areas = [
        ['area_cc_ia', 'Inteligência Artificial e Ciência de Dados', 'CC-IA', 'prog_xyzq_cc', 'Sistemas inteligentes, aprendizado de máquina e visão computacional'],
        ['area_cc_es', 'Engenharia de Software e Sistemas Distribuídos', 'CC-ES', 'prog_xyzq_cc', 'Arquitetura de software, computação em nuvem e segurança'],
        ['area_fis_mat', 'Física da Matéria Condensada', 'FIS-MAT', 'prog_xyzq_fis', 'Nanoestruturas, supercondutividade e novos materiais'],
        ['area_fis_rad', 'Física Nuclear e Radiológica', 'FIS-RAD', 'prog_xyzq_fis', 'Dosimetria, instrumentação nuclear e física médica'],
        ['area_bio_gen', 'Genômica e Bioinformática', 'BIO-GEN', 'prog_xyzq_bio', 'Sequenciamento genômico, expressão gênica e biologia computacional'],
        ['area_bio_fer', 'Processos Biotecnológicos e Fermentativos', 'BIO-FER', 'prog_xyzq_bio', 'Bioprocessos industriais e engenharia metabólica'],
        ['area_mpe_dev', 'Desenvolvimento Ágil e DevOps Avançado', 'MPE-DEV', 'prog_xyzq_mpe', 'Processos modernos de engenharia de software e automação'],
        ['area_mpe_gov', 'Governança Digital e Gestão de TI', 'MPE-GOV', 'prog_xyzq_mpe', 'Transformação digital, governança corporativa e produtos de TI'],
    ]
    write_csv(os.path.join(out, "04_areas_concentracao_op_program_concentration_area.csv"),
              ['id', 'name', 'code', 'program_id/id', 'description'], areas)

    # 05 Docentes: 25 professores com dados censitários completos e nomes únicos
    fac_records = []
    accred_records = []
    fac_ids = []
    for f_idx in range(1, 26):
        g_letter = 'm' if f_idx % 2 != 0 else 'f'
        ident = gen_unique_identity(f_idx + 10, g_letter, domain="xyzq.edu.br")
        fac_id = f"fac_xyzq_{f_idx:02d}"
        fac_ids.append(fac_id)
        orcid = f"0000-0002-1825-{f_idx:04d}"
        lattes = f"http://lattes.cnpq.br/{ident['cpf']}0001"
        b_year = 1968 + (f_idx % 20)
        
        fac_records.append([
            fac_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
            ident['cpf'], ident['email'], ident['phone'], ident['gender'], f"{b_year}-05-15",
            ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
            'base.br', 'exclusive', '40', 'phd', 'Ciência e Tecnologia', 'Universidade XYZQ',
            orcid, lattes, ident['street'], ident['city'], ident['zip']
        ])
    
    write_csv(os.path.join(out, "05_docentes_orientadores_op_faculty.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'gender', 'birth_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'work_regime', 'workload', 'degree_level', 'degree_area', 'degree_ies', 'orcid', 'lattes_url', 'street', 'city', 'zip'], fac_records)

    prog_fac_map = {
        'prog_xyzq_cc': fac_ids[0:13],
        'prog_xyzq_fis': fac_ids[6:19],
        'prog_xyzq_bio': fac_ids[12:25],
        'prog_xyzq_mpe': fac_ids[0:5] + fac_ids[7:10] + fac_ids[19:24]
    }
    accred_idx = 1
    for p_id, f_list in prog_fac_map.items():
        for fid in f_list:
            accred_records.append([f"accred_{accred_idx:03d}", fid, p_id, 'permanent', '2022-01-01', ''])
            accred_idx += 1
    write_csv(os.path.join(out, "06_credenciamento_docente_cpg_op_faculty_accreditation.csv"),
              ['id', 'faculty_id/id', 'program_id/id', 'category', 'date_start', 'date_end'], accred_records)

    # 07 Subjects
    subjects = []
    subj_by_prog = {
        'prog_xyzq_cc': [
            ('CC501', 'Metodologia de Pesquisa em Computação', 'compulsory', 4, 60),
            ('CC502', 'Algoritmos Avançados e Teoria da Computação', 'compulsory', 4, 60),
            ('CC503', 'Seminários de Computação Científica', 'compulsory', 2, 30),
            ('CC510', 'Aprendizado Profundo e Redes Neurais', 'elective', 4, 60),
            ('CC511', 'Processamento de Linguagem Natural', 'elective', 4, 60),
            ('CC512', 'Visão Computacional e Reconhecimento de Padrões', 'elective', 4, 60),
            ('CC520', 'Sistemas Distribuídos e Computação em Nuvem', 'elective', 4, 60),
            ('CC521', 'Engenharia de Requisitos e Modelagem Ágil', 'elective', 4, 60),
            ('CC522', 'Cibersegurança e Criptografia Aplicada', 'elective', 4, 60),
        ],
        'prog_xyzq_fis': [
            ('FA601', 'Mecânica Quântica Avançada', 'compulsory', 4, 60),
            ('FA602', 'Métodos Matemáticos da Física Teórica', 'compulsory', 4, 60),
            ('FA603', 'Seminário Geral de Física Aplicada', 'compulsory', 2, 30),
            ('FA610', 'Física de Sólidos e Semicondutores', 'elective', 4, 60),
            ('FA611', 'Espectroscopia e Difração de Raios-X', 'elective', 4, 60),
            ('FA612', 'Nanotecnologia e Superfícies', 'elective', 4, 60),
            ('FA620', 'Interação da Radiação com a Matéria', 'elective', 4, 60),
            ('FA621', 'Física Médica e Radioterapia Computacional', 'elective', 4, 60),
            ('FA622', 'Detectores Nucleares e Processamento de Sinais', 'elective', 4, 60),
        ],
        'prog_xyzq_bio': [
            ('BM701', 'Biologia Molecular Celular Avançada', 'compulsory', 4, 60),
            ('BM702', 'Bioestatística e Delineamento Experimental', 'compulsory', 4, 60),
            ('BM703', 'Seminários Integrados em Biotecnologia', 'compulsory', 2, 30),
            ('BM710', 'Bioinformática e Análise de Sequências NGS', 'elective', 4, 60),
            ('BM711', 'Genômica Funcional e Epigenética', 'elective', 4, 60),
            ('BM712', 'Engenharia de Proteínas e Cristalografia', 'elective', 4, 60),
            ('BM720', 'Biotecnologia da Fermentação e Biorreatores', 'elective', 4, 60),
            ('BM721', 'Purificação de Biomoléculas e Downstream', 'elective', 4, 60),
            ('BM722', 'Bioprodutos e Biocombustíveis Avançados', 'elective', 4, 60),
        ],
        'prog_xyzq_mpe': [
            ('ES801', 'Metodologia de PTT e Inovação Tecnológica', 'compulsory', 4, 60),
            ('ES802', 'Arquitetura de Software e Microsserviços', 'compulsory', 4, 60),
            ('ES803', 'Seminário de Projetos Tecnológicos', 'compulsory', 2, 30),
            ('ES810', 'Engenharia de Plataforma e Práticas DevOps/SRE', 'elective', 4, 60),
            ('ES811', 'Testes Automatizados e Qualidade de Software', 'elective', 4, 60),
            ('ES812', 'Desenvolvimento Cloud-Native e Containers', 'elective', 4, 60),
            ('ES820', 'Governança Digital e LGPD em Sistemas de TI', 'elective', 4, 60),
            ('ES821', 'Gestão de Produtos Digitais e Design de Serviços', 'elective', 4, 60),
            ('ES822', 'Gestão Ágil de Portfólio e Métricas de Software', 'elective', 4, 60),
        ],
    }

    sub_lookup = {}
    for p_id, sub_list in subj_by_prog.items():
        sub_lookup[p_id] = []
        for code, sname, stype, creds, hrs in sub_list:
            sid = f"sub_{code.lower()}"
            sub_lookup[p_id].append((code, sname, stype, creds, hrs))
            subjects.append([sid, sname, code, 'theory', stype, p_id, creds])
    write_csv(os.path.join(out, "07_disciplinas_catalogo_op_subject.csv"),
              ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'], subjects)

    # 08 Editais
    editais = [
        ['edital_xyzq_cc_2024', 'Edital PPGCC 2024', 'EDITAL-PPGCC-2024', 'prog_xyzq_cc', 'reg_xyzq_cc_2024', '2024', '20', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_fis_2024', 'Edital PPGFA 2024', 'EDITAL-PPGFA-2024', 'prog_xyzq_fis', 'reg_xyzq_fis_2024', '2024', '15', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_bio_2024', 'Edital PPGBM 2024', 'EDITAL-PPGBM-2024', 'prog_xyzq_bio', 'reg_xyzq_bio_2024', '2024', '18', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_mpe_2024', 'Edital MPESI 2024', 'EDITAL-MPESI-2024', 'prog_xyzq_mpe', 'reg_xyzq_mpe_2024', '2024', '25', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
    ]
    write_csv(os.path.join(out, "08_editais_selecao_op_admission_edital.csv"),
              ['id', 'name', 'code', 'program_id/id', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'], editais)

    # 09 Students across Programs with 100% Unique Full Names
    students = []
    courses = []
    ledger = []
    theses = []
    ptts = []
    
    stu_idx_global = 100
    for p_idx, (p_id, prog_name, short_code, _, p_modal, _, _, _) in enumerate(progs, 1):
        reg_id = f"reg_{p_id.replace('prog_', '')}_2024"
        n_students = 20 if p_modal == 'academic' else 25
        subj_list = sub_lookup[p_id]
        
        for s_idx in range(1, n_students + 1):
            stu_idx_global += 1
            g_letter = 'f' if (stu_idx_global % 2 == 0) else 'm'
            ident = gen_unique_identity(stu_idx_global, g_letter, domain="aluno.xyzq.edu.br")
            
            stu_id = f"stu_{short_code.lower()}_{s_idx:02d}"
            ra = f"RA2024{p_idx}{s_idx:03d}"
            is_alumni = (s_idx <= 8)
            cat = 'alumni' if is_alumni else 'regular'
            capes_st = 'graduated' if is_alumni else 'enrolled'
            state = 'finished' if is_alumni else 'running'
            end_date = '2026-03-31' if is_alumni else ''
            
            students.append([
                stu_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
                ident['cpf'], ident['email'], ident['phone'], ra, ra, comp_id, cat, capes_st,
                'f' if g_letter == 'f' else 'm', f"{1993 + (s_idx % 7)}-08-14", '2024-03-01',
                ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
                'base.br', 'bachelor', 'grad',
                f"0000-0002-{stu_idx_global:04d}-{(stu_idx_global * 9) % 9000:04d}",
                f"http://lattes.cnpq.br/{ident['cpf']}0002",
                ident['street'], ident['city'], ident['zip'], 'approved', 'not_applicable'
            ])
            
            courses.append([f"course_{stu_id}", stu_id, p_id, f"batch_{p_id}_2024", p_id, reg_id, 'regular', state, '2024-03-01', end_date])

            # Livro-Razão
            for code, sname, stype, creds, hrs in subj_list[:5]:
                sid = f"sub_{code.lower()}"
                ledger.append([
                    f"led_{stu_id}_{code.lower()}", stu_id, reg_id, sid, sname,
                    'subject_internal', creds, hrs, 'A' if s_idx % 2 == 0 else 'B', 'True', '2024-06-30', 'Semestre 1'
                ])

            if is_alumni:
                ledger.append([f"led_{stu_id}_apo", stu_id, reg_id, '', 'Atividades Complementares e Produção', 'apo', '8', '120', 'A', 'True', '2025-11-30', 'APO'])
                ledger.append([f"led_{stu_id}_def", stu_id, reg_id, '', 'Defesa de Tese / Dissertação', 'milestone', '52', '780', 'A', 'True', '2026-03-31', 'Defesa'])
                
                th_id = f"thesis_{stu_id}"
                th_title = f"Investigação Avançada e Desenvolvimento em {short_code} - Discente {ident['last_name']}"
                adv_id = RNG.choice(prog_fac_map[p_id])
                theses.append([th_id, stu_id, f"wp_{stu_id}", reg_id, th_title, 'dissertation', 'defense', 'homologated', '2026-03-31', f"http://repositorio.xyzq.edu.br/{stu_id}", adv_id])

                if p_modal == 'professional':
                    ptt_id = f"ptt_{stu_id}"
                    ptt_name = f"Plataforma de Software Aplicada {short_code}-{s_idx}"
                    ptts.append([ptt_id, ptt_name, ptt_name, th_id, stu_id, '1', 'T19', 'T1', 'trl_7', 'Aderente à Linha de Engenharia de Software', 'homologated'])

    write_csv(os.path.join(out, "09_discentes_identidade_op_student.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'english_proficiency_status', 'portuguese_proficiency_status'], students)
    write_csv(os.path.join(out, "10_vinculos_curso_op_student_course.csv"),
              ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'], courses)
    write_csv(os.path.join(out, "11_livro_razao_historico_op_student_credit_ledger.csv"),
              ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'], ledger)
    write_csv(os.path.join(out, "12_bancas_defesas_capes_thesis.csv"),
              ['id', 'student_id/id', 'work_plan_id/id', 'curriculum_version_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url', 'advisor_id/id'], theses)
    write_csv(os.path.join(out, "13_produtos_ptt_capes_ptt_product.csv"),
              ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'axis_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'], ptts)

# ------------------------------------------------------------------------------
# SCENARIO 2: MPTRCS / IPEN-CNEN/SP
# ------------------------------------------------------------------------------
def generate_scenario_mptrcs(base_dir):
    print("--- Generating Scenario 2: MPTRCS / IPEN-CNEN/SP ---")
    out = os.path.join(base_dir, "mptrcs_ipen")
    comp_id = "comp_ies_ipen"
    p_id = "prog_mptrcs"
    reg_id = "reg_mptrcs_v2"
    
    # 01 Company
    write_csv(os.path.join(out, "01_ies_instituicao_res_company.csv"),
              ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
              [[comp_id, 'Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP', '00.394.429/0001-00', '1902', 'Av. Prof. Lineu Prestes, 2242 - Cidade Universitária', 'São Paulo', '05508-000', 'BR']])

    # 02 Program
    write_csv(os.path.join(out, "02_programas_capes_op_program.csv"),
              ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id'],
              [[p_id, 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde', 'MPTRCS', '33002010001P0', 'professional', '4', 'semestral', comp_id]])

    # 03 Curriculum Version
    write_csv(os.path.join(out, "03_versao_curricular_op_curriculum_version.csv"),
              ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'],
              [[reg_id, 'Regulamento MP-TRCS v2 (2024)', p_id, '100', '40', '52', '8', '15', '50', '24', 'False', '0', '36', 'cpg_approval', 'omit_on_regular', 'False', '0', 'True', 'current_matrix', 'scale_abc_r', 'admission', 'not_applicable', 'cpg_checklist', 'hybrid_allowed']])

    # 04 Áreas de Concentração
    areas = [
        ['area_rad_dos', 'Radioterapia e Dosimetria das Radiações', 'RAD-DOS', p_id, 'Física médica, dosimetria e controle de qualidade em radioterapia'],
        ['area_rad_nuc', 'Medicina Nuclear e Radiofarmácia', 'RAD-NUC', p_id, 'Radiofármacos inovadores, imunologia molecular e dosimetria interna'],
    ]
    write_csv(os.path.join(out, "04_areas_concentracao_op_program_concentration_area.csv"),
              ['id', 'name', 'code', 'program_id/id', 'description'], areas)

    # 05 Docentes: 12 professores com dados censitários completos e nomes únicos
    fac_records = []
    accred_records = []
    fac_ids = []
    for f_idx in range(1, 13):
        g_letter = 'm' if f_idx % 2 != 0 else 'f'
        ident = gen_unique_identity(f_idx + 80, g_letter, domain="ipen.br")
        fac_id = f"fac_mptrcs_{f_idx:02d}"
        fac_ids.append(fac_id)
        orcid = f"0000-0001-9000-{f_idx:04d}"
        lattes = f"http://lattes.cnpq.br/{ident['cpf']}0001"
        b_year = 1965 + (f_idx % 18)
        
        fac_records.append([
            fac_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
            ident['cpf'], ident['email'], ident['phone'], ident['gender'], f"{b_year}-04-12",
            ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
            'base.br', 'exclusive' if f_idx % 3 != 0 else 'fulltime', '40', 'phd',
            'Tecnologia Nuclear e Radiológica', 'Universidade de São Paulo - USP',
            orcid, lattes, ident['street'], ident['city'], ident['zip']
        ])
        accred_records.append([f"accred_mptrcs_{f_idx:02d}", fac_id, p_id, 'permanent', '2021-01-01', ''])

    write_csv(os.path.join(out, "05_docentes_orientadores_op_faculty.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'gender', 'birth_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'work_regime', 'workload', 'degree_level', 'degree_area', 'degree_ies', 'orcid', 'lattes_url', 'street', 'city', 'zip'], fac_records)
    write_csv(os.path.join(out, "06_credenciamento_docente_cpg_op_faculty_accreditation.csv"),
              ['id', 'faculty_id/id', 'program_id/id', 'category', 'date_start', 'date_end'], accred_records)

    # 07 Subjects
    subjects = [
        ['sub_mptrcs_rad501', 'Fundamentos de Radiobiologia e Proteção Radiológica', 'RAD501', 'theory', 'compulsory', p_id, 4],
        ['sub_mptrcs_rad502', 'Metodologia Científica e Elaboração de PTT', 'RAD502', 'theory', 'compulsory', p_id, 4],
        ['sub_mptrcs_rad503', 'Seminários Gerais em Tecnologia das Radiações', 'RAD503', 'theory', 'compulsory', p_id, 2],
        ['sub_mptrcs_rad510', 'Dosimetria Física e Clínica em Radioterapia', 'RAD510', 'theory', 'elective', p_id, 4],
        ['sub_mptrcs_rad511', 'Controle de Qualidade em Aceleradores Lineares', 'RAD511', 'theory', 'elective', p_id, 4],
        ['sub_mptrcs_rad512', 'Braquiterapia Avançada e Implante de Sementes', 'RAD512', 'theory', 'elective', p_id, 4],
        ['sub_mptrcs_rad520', 'Radiofarmácia e Radioimunologia', 'RAD520', 'theory', 'elective', p_id, 4],
        ['sub_mptrcs_rad521', 'Instrumentação em PET/SPECT e Imagem Molecular', 'RAD521', 'theory', 'elective', p_id, 4],
        ['sub_mptrcs_rad522', 'Gerenciamento de Rejeitos Radioativos em Serviços de Saúde', 'RAD522', 'theory', 'elective', p_id, 4],
    ]
    write_csv(os.path.join(out, "07_disciplinas_catalogo_op_subject.csv"),
              ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'], subjects)

    # 08 Editais
    editais = [
        ['edital_mptrcs_t1', 'Edital Processo Seletivo MPTRCS - Turma 1 (2022)', 'EDITAL-MPTRCS-2022', p_id, reg_id, '2022', '15', '2021-10-01', '2021-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t2', 'Edital Processo Seletivo MPTRCS - Turma 2 (2023)', 'EDITAL-MPTRCS-2023', p_id, reg_id, '2023', '15', '2022-10-01', '2022-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t3', 'Edital Processo Seletivo MPTRCS - Turma 3 (2024)', 'EDITAL-MPTRCS-2024', p_id, reg_id, '2024', '15', '2023-10-01', '2023-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t4', 'Edital Processo Seletivo MPTRCS - Turma 4 (2025)', 'EDITAL-MPTRCS-2025', p_id, reg_id, '2025', '15', '2024-10-01', '2024-12-15', '20.0', 'published'],
    ]
    write_csv(os.path.join(out, "08_editais_selecao_op_admission_edital.csv"),
              ['id', 'name', 'code', 'program_id/id', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'], editais)

    # 09 Discentes: 60 alunos em 4 turmas com NOMES 100% ÚNICOS
    students = []
    courses = []
    ledger = []
    theses = []
    ptts = []

    t_cfg = [
        (1, 2022, 15, 0),
        (2, 2023, 15, 0),
        (3, 2024, 12, 3),
        (4, 2025, 0, 15),
    ]

    mptrcs_stu_counter = 0
    for t_num, year, n_tit, n_cur in t_cfg:
        for s_idx in range(1, 16):
            mptrcs_stu_counter += 1
            g_letter = 'f' if (mptrcs_stu_counter % 2 == 0) else 'm'
            ident = gen_unique_identity(mptrcs_stu_counter + 300, g_letter, domain="ipen.br")
            
            stu_id = f"stu_mptrcs_t{t_num}_{s_idx:02d}"
            ra = f"RA{year}{s_idx:03d}"
            is_alumni = (s_idx <= n_tit)
            cat = 'alumni' if is_alumni else 'regular'
            capes_st = 'graduated' if is_alumni else 'enrolled'
            state = 'finished' if is_alumni else 'running'
            end_date = f"{year+2}-04-15" if is_alumni else ''
            b_year = 1991 + (mptrcs_stu_counter % 9)

            students.append([
                stu_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
                ident['cpf'], ident['email'], ident['phone'], ra, ra, comp_id, cat, capes_st,
                'f' if g_letter == 'f' else 'm', f"{b_year}-07-22", f"{year}-03-01",
                ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
                'base.br', 'bachelor', 'grad',
                f"0000-0002-{mptrcs_stu_counter + 4000:04d}-{(mptrcs_stu_counter * 13) % 9000:04d}",
                f"http://lattes.cnpq.br/{ident['cpf']}0002",
                ident['street'], ident['city'], ident['zip'], 'approved', 'not_applicable'
            ])

            courses.append([f"link_{stu_id}", stu_id, p_id, f"batch_mptrcs_t{t_num}", p_id, reg_id, 'regular', state, f"{year}-03-01", end_date])

            # Livro-Razão
            # Obrigatórias
            for sid, sname, code, _, _, _, creds in subjects[:3]:
                ledger.append([
                    f"led_{stu_id}_{code.lower()}", stu_id, reg_id, f"sub_mptrcs_{code.lower()}", sname,
                    'subject_internal', creds, creds * 15, 'A' if s_idx % 2 == 0 else 'B', 'True', f"{year}-06-30", f"Turma {t_num} Sem 1"
                ])

            # Eletivas
            if is_alumni or t_num == 3:
                for sid, sname, code, _, _, _, creds in subjects[3:]:
                    ledger.append([
                        f"led_{stu_id}_{code.lower()}", stu_id, reg_id, f"sub_mptrcs_{code.lower()}", sname,
                        'subject_internal', creds, creds * 15, 'A' if s_idx % 3 != 0 else 'B', 'True', f"{year}-12-15", f"Turma {t_num} Sem 2"
                    ])

            if is_alumni:
                ledger.append([f"led_{stu_id}_apo", stu_id, reg_id, '', 'Seminários de Acompanhamento e Desenvolvimento de PTT', 'apo', '8', '120', 'A', 'True', f"{year+1}-11-30", f"Turma {t_num} APO"])
                ledger.append([f"led_{stu_id}_def", stu_id, reg_id, '', 'Defesa Pública de Dissertação e Produto Tecnológico', 'milestone', '52', '780', 'A', 'True', f"{year+2}-04-15", f"Turma {t_num} Defesa"])

                adv_id = RNG.choice(fac_ids)
                th_id = f"thesis_{stu_id}"
                th_title = f"Otimização Dosimétrica e Inovação Tecnológica em Feixes Clínicos - Estudo {ident['last_name']}"
                theses.append([th_id, stu_id, f"wp_{stu_id}", reg_id, th_title, 'dissertation', 'defense', 'homologated', f"{year+2}-04-15", f"http://repositorio.ipen.br/handle/123456789/{mptrcs_stu_counter}", adv_id])

                ptt_id = f"ptt_{stu_id}"
                ptt_name = f"Inovação Tecnológica Aplicada MPTRCS: Software Dosimétrico ({ident['last_name']})"
                qualis = 'T1' if s_idx % 3 == 0 else ('T2' if s_idx % 2 == 0 else 'T3')
                trl = f"trl_{min(9, 6 + (s_idx % 4))}"
                ptts.append([ptt_id, ptt_name, ptt_name, th_id, stu_id, '1', 'T19', qualis, trl, 'Aderente à Linha de Radioterapia e Dosimetria', 'homologated'])

    write_csv(os.path.join(out, "09_discentes_identidade_op_student.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'english_proficiency_status', 'portuguese_proficiency_status'], students)
    write_csv(os.path.join(out, "10_vinculos_curso_op_student_course.csv"),
              ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'], courses)
    write_csv(os.path.join(out, "11_livro_razao_historico_op_student_credit_ledger.csv"),
              ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'], ledger)
    write_csv(os.path.join(out, "12_bancas_defesas_capes_thesis.csv"),
              ['id', 'student_id/id', 'work_plan_id/id', 'curriculum_version_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url', 'advisor_id/id'], theses)
    write_csv(os.path.join(out, "13_produtos_ptt_capes_ptt_product.csv"),
              ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'axis_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'], ptts)

# ------------------------------------------------------------------------------
# STANDARDIZED SKELETON TEMPLATES
# ------------------------------------------------------------------------------
def generate_standard_skeletons(base_dir):
    print("--- Generating Standardized Skeletons ---")
    out = os.path.join(base_dir, "esqueletos_padronizados")
    
    skeletons = {
        "01_ies_instituicao_res_company.csv": ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
        "02_programas_capes_op_program.csv": ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id'],
        "03_versao_curricular_op_curriculum_version.csv": ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'],
        "04_areas_concentracao_op_program_concentration_area.csv": ['id', 'name', 'code', 'program_id/id', 'description'],
        "05_docentes_orientadores_op_faculty.csv": ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'gender', 'birth_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'work_regime', 'workload', 'degree_level', 'degree_area', 'degree_ies', 'orcid', 'lattes_url', 'street', 'city', 'zip'],
        "06_credenciamento_docente_cpg_op_faculty_accreditation.csv": ['id', 'faculty_id/id', 'program_id/id', 'category', 'date_start', 'date_end'],
        "07_disciplinas_catalogo_op_subject.csv": ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'],
        "08_editais_selecao_op_admission_edital.csv": ['id', 'name', 'code', 'program_id/id', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'],
        "09_discentes_identidade_op_student.csv": ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'english_proficiency_status', 'portuguese_proficiency_status'],
        "10_vinculos_curso_op_student_course.csv": ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'],
        "11_livro_razao_historico_op_student_credit_ledger.csv": ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'],
        "12_bancas_defesas_capes_thesis.csv": ['id', 'student_id/id', 'work_plan_id/id', 'curriculum_version_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url', 'advisor_id/id'],
        "13_produtos_ptt_capes_ptt_product.csv": ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'axis_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'],
    }
    
    for filename, headers in skeletons.items():
        write_csv(os.path.join(out, filename), headers, [])

if __name__ == '__main__':
    base_dir = 'import_templates'
    generate_scenario_xyzq(os.path.join(base_dir, 'datasets_sinteticos'))
    generate_scenario_mptrcs(os.path.join(base_dir, 'datasets_sinteticos'))
    generate_standard_skeletons(base_dir)
    print('[SUCCESS] All synthetic datasets and skeletons regenerated with 100% compliant schemas and unique names!')
