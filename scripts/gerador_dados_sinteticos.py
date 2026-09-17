#!/usr/bin/env python3
"""
Procedural Synthetic Data Generator for l10n_br_openeducat_capes (Odoo 19.0)
Scenarios:
1. Universidade XYZQ (3 Academic Programs + 1 Professional Program with cohorts T1-T9)
2. MPTRCS / IPEN-CNEN/SP (Reference profile with external registration at USP)

Generates complete, non-repeating, realistic Brazilian academic datasets
with 100% of CAPES census fields (mother name, race/color, disability, birth city/state,
nationality, PIDs, degrees, work regimes), distinct first_name, middle_name, last_name,
and strict foreign key relational integrity against OpenEduCat 19 and CAPES models.
"""

import os
import csv
import base64
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
# SCENARIO 1: UNIVERSIDADE XYZQ (4 PROGRAMAS: 3 ACADÊMICOS + 1 PROFISSIONAL)
# ------------------------------------------------------------------------------
def generate_scenario_xyzq(base_dir):
    print("--- Generating Scenario 1: Universidade XYZQ ---")
    out = os.path.join(base_dir, "universidade_xyzq")
    comp_id = "comp_ies_xyzq"
    dummy_pdf = base64.b64encode(b"%PDF-1.4 Mock Plano de Trabalho Universidade XYZQ").decode('utf-8')
    
    # 01a Company
    write_csv(os.path.join(out, "01a_ies_instituicao_res_company.csv"),
              ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
              [[comp_id, 'Universidade XYZQ', '12.345.678/0001-90', '12345', 'Av. Central Universitária, 1000', 'São Paulo', '01000-000', 'BR']])

    # 01b Departamentos OpenEduCat (op.department)
    depts = [
        ['dept_xyzq_dcc', 'Departamento de Ciência da Computação', 'DCC-XYZQ'],
        ['dept_xyzq_dfis', 'Departamento de Física Aplicada', 'DFIS-XYZQ'],
        ['dept_xyzq_dbio', 'Departamento de Biotecnologia e Biologia Molecular', 'DBIO-XYZQ'],
        ['dept_xyzq_desi', 'Departamento de Engenharia de Software e Inovação', 'DESI-XYZQ'],
        ['dept_xyzq_cpg', 'Comissão Central de Pós-Graduação (CPG-XYZQ)', 'CPG-XYZQ'],
        ['dept_xyzq_sec', 'Secretaria Geral de Pós-Graduação (SECPG)', 'SECPG-XYZQ'],
    ]
    write_csv(os.path.join(out, "01b_departamentos_op_department.csv"),
              ['id', 'name', 'code'], depts)

    # 01c Categorias OpenEduCat (op.category)
    cats = [
        ['cat_xyzq_reg', 'Aluno Regular Stricto Sensu', 'REG-XYZQ', comp_id],
        ['cat_xyzq_esp', 'Aluno Especial / Disciplinas Isoladas', 'ESP-XYZQ', comp_id],
        ['cat_xyzq_doc_perm', 'Docente Permanente CPG', 'DOC-PERM', comp_id],
        ['cat_xyzq_doc_colab', 'Docente Colaborador', 'DOC-COLAB', comp_id],
        ['cat_xyzq_rep_disc', 'Representante Discente CPG', 'REP-DISC', comp_id],
    ]
    write_csv(os.path.join(out, "01c_categorias_op_category.csv"),
              ['id', 'name', 'code', 'company_id/id'], cats)

    # 01d Anos Acadêmicos (op.academic.year)
    years = []
    for y in range(2022, 2027):
        years.append([f"ay_xyzq_{y}", f"Ano Acadêmico {y}", f"{y}-01-01", f"{y}-12-31", 'two_sem', comp_id])
    write_csv(os.path.join(out, "01d_anos_academicos_op_academic_year.csv"),
              ['id', 'name', 'start_date', 'end_date', 'term_structure', 'company_id/id'], years)

    # 01e Termos Letivos / Semestres (op.academic.term)
    terms = []
    for y in range(2022, 2027):
        terms.append([f"term_xyzq_{y}_1", f"{y}.1", f"ay_xyzq_{y}", f"{y}-02-01", f"{y}-06-30", comp_id])
        terms.append([f"term_xyzq_{y}_2", f"{y}.2", f"ay_xyzq_{y}", f"{y}-08-01", f"{y}-12-15", comp_id])
    write_csv(os.path.join(out, "01e_termos_academicos_op_academic_term.csv"),
              ['id', 'name', 'academic_year_id/id', 'term_start_date', 'term_end_date', 'company_id/id'], terms)

    # 01f Níveis de Programa (op.program.level)
    levels = [
        ['level_xyzq_acad', 'Pós-Graduação Stricto Sensu - Mestrado e Doutorado Acadêmico'],
        ['level_xyzq_prof', 'Pós-Graduação Stricto Sensu - Mestrado Profissional'],
    ]
    write_csv(os.path.join(out, "01f_niveis_programa_op_program_level.csv"),
              ['id', 'name'], levels)

    # 01g Programas OpenEduCat (op.program)
    oe_progs = [
        ['prog_oe_ppgcc', 'Programa de Pós-Graduação em Ciência da Computação', 'PPGCC', 'level_xyzq_acad', 'dept_xyzq_dcc', 'True'],
        ['prog_oe_ppgfa', 'Programa de Pós-Graduação em Física Aplicada', 'PPGFA', 'level_xyzq_acad', 'dept_xyzq_dfis', 'True'],
        ['prog_oe_ppgbm', 'Programa de Pós-Graduação em Biotecnologia Molecular', 'PPGBM', 'level_xyzq_acad', 'dept_xyzq_dbio', 'True'],
        ['prog_oe_mpesi', 'Mestrado Profissional em Engenharia de Software e Inovação', 'MPESI', 'level_xyzq_prof', 'dept_xyzq_desi', 'True'],
    ]
    write_csv(os.path.join(out, "01g_programas_openeducat_op_program.csv"),
              ['id', 'name', 'code', 'program_level_id/id', 'department_id/id', 'active'], oe_progs)

    # 01h Cursos OpenEduCat (op.course)
    courses = [
        ['crs_xyzq_cc', 'Curso de Ciência da Computação (Stricto Sensu)', 'CRS-PPGCC', 'normal', 'prog_oe_ppgcc', 'dept_xyzq_dcc'],
        ['crs_xyzq_fis', 'Curso de Física Aplicada (Stricto Sensu)', 'CRS-PPGFA', 'normal', 'prog_oe_ppgfa', 'dept_xyzq_dfis'],
        ['crs_xyzq_bio', 'Curso de Biotecnologia Molecular (Stricto Sensu)', 'CRS-PPGBM', 'normal', 'prog_oe_ppgbm', 'dept_xyzq_dbio'],
        ['crs_xyzq_mpe', 'Curso de Engenharia de Software e Inovação (Mestrado Profissional)', 'CRS-MPESI', 'normal', 'prog_oe_mpesi', 'dept_xyzq_desi'],
    ]
    write_csv(os.path.join(out, "01h_cursos_openeducat_op_course.csv"),
              ['id', 'name', 'code', 'evaluation_type', 'program_id/id', 'department_id/id'], courses)

    # 01i Lotes / Turmas (op.batch)
    batches = [
        ['batch_xyzq_cc_2024', 'Turma PPGCC 2024', 'PPGCC-2024', 'crs_xyzq_cc', '2024-03-01', '2026-03-31', 'True'],
        ['batch_xyzq_fis_2024', 'Turma PPGFA 2024', 'PPGFA-2024', 'crs_xyzq_fis', '2024-03-01', '2026-03-31', 'True'],
        ['batch_xyzq_bio_2024', 'Turma PPGBM 2024', 'PPGBM-2024', 'crs_xyzq_bio', '2024-03-01', '2026-03-31', 'True'],
        ['batch_xyzq_mpe_2024', 'Turma MPESI 2024', 'MPESI-2024', 'crs_xyzq_mpe', '2024-03-01', '2026-03-31', 'True'],
    ]
    write_csv(os.path.join(out, "01i_lotes_turmas_op_batch.csv"),
              ['id', 'name', 'code', 'course_id/id', 'start_date', 'end_date', 'active'], batches)

    # 02 Programas CAPES (op.program.capes)
    progs = [
        ['prog_xyzq_cc', 'Programa de Pós-Graduação em Ciência da Computação', 'PPGCC', '33001010001P1', 'academic', '5', 'semestral', comp_id, 'Ciência da Computação', 'active'],
        ['prog_xyzq_fis', 'Programa de Pós-Graduação em Física Aplicada', 'PPGFA', '33001010002P8', 'academic', '6', 'semestral', comp_id, 'Astronomia / Física', 'active'],
        ['prog_xyzq_bio', 'Programa de Pós-Graduação em Biotecnologia Molecular', 'PPGBM', '33001010003P4', 'academic', '5', 'semestral', comp_id, 'Biotecnologia', 'active'],
        ['prog_xyzq_mpe', 'Mestrado Profissional em Engenharia de Software e Inovação', 'MPESI', '33001010004P0', 'professional', '4', 'semestral', comp_id, 'Engenharia / Software', 'active'],
    ]
    write_csv(os.path.join(out, "02_programas_capes_op_program.csv"),
              ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id', 'evaluation_area', 'status'], progs)

    # 03 Versão Curricular (op.curriculum.version)
    regs = [
        ['reg_xyzq_cc_2024', 'Regimento PPGCC 2024', 'prog_xyzq_cc', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_fis_2024', 'Regimento PPGFA 2024', 'prog_xyzq_fis', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_bio_2024', 'Regimento PPGBM 2024', 'prog_xyzq_bio', '100', '40', '52', '8', '15', '50', '24', 'True', '2', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'qualification', 'mandatory_all', 'none', 'hybrid_allowed'],
        ['reg_xyzq_mpe_2024', 'Regimento MPESI 2024', 'prog_xyzq_mpe', '100', '40', '52', '8', '15', '50', '24', 'False', '0', '36', 'cpg_approval', 'omit_on_regular', 'True', '30', 'True', 'current_matrix', 'scale_abc_r', 'admission', 'not_applicable', 'cpg_checklist', 'hybrid_allowed'],
    ]
    write_csv(os.path.join(out, "03_versao_curricular_op_curriculum_version.csv"),
              ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'], regs)

    # 04a Áreas de Concentração (op.program.concentration.area)
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
    write_csv(os.path.join(out, "04a_areas_concentracao_op_program_concentration_area.csv"),
              ['id', 'name', 'code', 'program_id/id', 'description'], areas)

    # 04b Linhas de Pesquisa (op.program.research.line)
    lines = [
        ['line_cc_ia_01', 'Aprendizado de Máquina e Modelos Generativos', 'IA-01', 'area_cc_ia', 'Pesquisa em deep learning, LLMs e representações neurais'],
        ['line_cc_ia_02', 'Visão Computacional e Processamento de Imagens', 'IA-02', 'area_cc_ia', 'Reconhecimento de padrões biomédicos e análise de vídeo'],
        ['line_cc_es_01', 'Arquitetura de Software e Computação em Nuvem', 'ES-01', 'area_cc_es', 'Microsserviços, escalabilidade e tolerância a falhas'],
        ['line_cc_es_02', 'Cibersegurança e Criptografia Aplicada', 'ES-02', 'area_cc_es', 'Segurança defensiva, blockchain e verificação formal'],
        ['line_fis_mat_01', 'Nanoestruturas e Síntese de Novos Materiais', 'MAT-01', 'area_fis_mat', 'Grafeno, filmes finos e spintrônica'],
        ['line_fis_mat_02', 'Supercondutividade e Física do Estado Sólido', 'MAT-02', 'area_fis_mat', 'Fenômenos quânticos macroscópicos em baixas temperaturas'],
        ['line_fis_rad_01', 'Dosimetria das Radiações e Física Médica', 'RAD-01', 'area_fis_rad', 'Calibração dosimétrica e simulações Monte Carlo'],
        ['line_fis_rad_02', 'Instrumentação Nuclear e Detectores de Radiação', 'RAD-02', 'area_fis_rad', 'Sensores semicondutores e espectrometria gama'],
        ['line_bio_gen_01', 'Genômica Comparativa e NGS', 'GEN-01', 'area_bio_gen', 'Sequenciamento de genomas bacterianos e metagenômica'],
        ['line_bio_gen_02', 'Bioinformática Estrutural e Modelagem Molecular', 'GEN-02', 'area_bio_gen', 'Predição conformacional de proteínas e docking de fármacos'],
        ['line_bio_fer_01', 'Engenharia de Biorreatores e Fermentação', 'FER-01', 'area_bio_fer', 'Otimização de escala em processos fermentativos contínuos'],
        ['line_bio_fer_02', 'Engenharia Metabólica e Bioprodutos', 'FER-02', 'area_bio_fer', 'Edição gênica CRISPR para produção de biopolímeros'],
        ['line_mpe_dev_01', 'Engenharia de Plataforma e Práticas DevOps/SRE', 'DEV-01', 'area_mpe_dev', 'Infraestrutura como código, CI/CD e observabilidade'],
        ['line_mpe_dev_02', 'Desenvolvimento Cloud-Native e Microsserviços', 'DEV-02', 'area_mpe_dev', 'Containers, service mesh e arquiteturas orientadas a eventos'],
        ['line_mpe_gov_01', 'Governança Digital e Privacidade de Dados (LGPD)', 'GOV-01', 'area_mpe_gov', 'Auditoria de algoritmos, conformidade legal e gestão de riscos'],
        ['line_mpe_gov_02', 'Gestão Ágil de Produtos e Métricas de Software', 'GOV-02', 'area_mpe_gov', 'Discovery de produtos, métricas DORA e agilidade em escala'],
    ]
    write_csv(os.path.join(out, "04b_linhas_pesquisa_op_program_research_line.csv"),
              ['id', 'name', 'code', 'area_id/id', 'description'], lines)

    # 05 Docentes Orientadores (op.faculty) — 25 professores únicos
    fac_records = []
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

    # 06a Vínculos Docente-Programa (op.faculty.program.link)
    # 06b Livro-Razão de Credenciamento Docente (op.faculty.category.ledger)
    prog_fac_map = {
        'prog_xyzq_cc': fac_ids[0:13],
        'prog_xyzq_fis': fac_ids[6:19],
        'prog_xyzq_bio': fac_ids[12:25],
        'prog_xyzq_mpe': fac_ids[0:5] + fac_ids[7:10] + fac_ids[19:24]
    }
    link_records = []
    ledger_records = []
    link_idx = 1
    for p_id, f_list in prog_fac_map.items():
        for fid in f_list:
            link_id = f"link_{fid}_{p_id}"
            link_records.append([link_id, fid, p_id])
            ledger_records.append([
                f"fac_led_{link_idx:03d}", link_id, 'permanent', '2022-01-01', '',
                f"Portaria CPG-XYZQ {link_idx:03d}/2022", 'Credenciamento Permanente Docente Homologado'
            ])
            link_idx += 1

    write_csv(os.path.join(out, "06a_vinculos_docente_programa_op_faculty_program_link.csv"),
              ['id', 'faculty_id/id', 'program_id/id'], link_records)
    write_csv(os.path.join(out, "06b_credenciamento_docente_ledger_op_faculty_category_ledger.csv"),
              ['id', 'program_link_id/id', 'category', 'start_date', 'end_date', 'document_ref', 'notes'], ledger_records)

    # 07a Disciplinas do Catálogo (op.subject)
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

    subjects = []
    rules = []
    sub_lookup = {}
    for p_id, sub_list in subj_by_prog.items():
        sub_lookup[p_id] = []
        reg_id = f"reg_{p_id.replace('prog_', '')}_2024"
        for code, sname, stype, creds, hrs in sub_list:
            sid = f"sub_{code.lower()}"
            sub_lookup[p_id].append((code, sname, stype, creds, hrs))
            subjects.append([sid, sname, code, 'theory', stype, p_id, creds])
            rules.append([f"rule_{sid}", reg_id, sid, 'Geral do Programa', 'program' if stype == 'compulsory' else 'area'])
            
    write_csv(os.path.join(out, "07a_disciplinas_catalogo_op_subject.csv"),
              ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'], subjects)
    write_csv(os.path.join(out, "07b_regras_curriculares_op_curriculum_subject_rule.csv"),
              ['id', 'curriculum_version_id/id', 'subject_id/id', 'area_name', 'scope'], rules)

    # 07c Projetos de Pesquisa Institucionais (capes.research.project)
    research_projs = [
        ['proj_cc_01', 'Sistemas Inteligentes e Redes Neurais Convolucionais para Apoio ao Diagnóstico', 'prog_xyzq_cc', fac_ids[0], 'line_cc_ia_01', 'applied', 'FAPESP', '2022/11234-5', '2022-03-01', '2026-12-31', 'ongoing', 'Projeto de IA aplicada à saúde'],
        ['proj_cc_02', 'Arquiteturas Criptográficas Seguras para Redes em Nuvem Distribuídas', 'prog_xyzq_cc', fac_ids[1], 'line_cc_es_02', 'basic', 'CNPq', '304567/2022-1', '2022-03-01', '2026-12-31', 'ongoing', 'Cibersegurança e protocolos pós-quânticos'],
        ['proj_fis_01', 'Propriedades Eletrônicas e Térmicas de Nanoestruturas Bidimensionais', 'prog_xyzq_fis', fac_ids[6], 'line_fis_mat_01', 'basic', 'CNPq', '401234/2022-8', '2022-03-01', '2026-12-31', 'ongoing', 'Estudo de materiais 2D e spintrônica'],
        ['proj_fis_02', 'Desenvolvimento de Novos Fantomas e Detectores para Dosimetria Clínica', 'prog_xyzq_fis', fac_ids[7], 'line_fis_rad_01', 'applied', 'FAPESP', '2022/23456-9', '2022-03-01', '2026-12-31', 'ongoing', 'Instrumentação radiológica de alta precisão'],
        ['proj_bio_01', 'Bioinformática Aplicada à Caracterização Genômica de Isolados Clínicos', 'prog_xyzq_bio', fac_ids[12], 'line_bio_gen_01', 'applied', 'CAPES', '88887.123456/2022-00', '2022-03-01', '2026-12-31', 'ongoing', 'Metagenômica e resistência bacteriana'],
        ['proj_bio_02', 'Otimização Metabólica para Bioprodução de Biopolímeros Industriais', 'prog_xyzq_bio', fac_ids[13], 'line_bio_fer_02', 'applied', 'FINEP', '01.22.0150.00', '2022-03-01', '2026-12-31', 'ongoing', 'Engenharia de bioprocessos sustentáveis'],
        ['proj_mpe_01', 'Plataformas de Automação DevOps e Observabilidade para Microsserviços', 'prog_xyzq_mpe', fac_ids[19], 'line_mpe_dev_01', 'applied', 'CNPq', '409876/2022-5', '2022-03-01', '2026-12-31', 'ongoing', 'Engenharia de software moderna e automação'],
        ['proj_mpe_02', 'Governança Digital e Conformidade com a LGPD em Arquiteturas Corporativas', 'prog_xyzq_mpe', fac_ids[20], 'line_mpe_gov_01', 'applied', 'FINEP', '01.22.0200.00', '2022-03-01', '2026-12-31', 'ongoing', 'Modelos de conformidade e privacidade'],
    ]
    write_csv(os.path.join(out, "07c_projetos_pesquisa_capes_research_project.csv"),
              ['id', 'name', 'program_id/id', 'coordinator_id/id', 'research_line_id/id', 'research_nature', 'funding_agency', 'funding_process', 'start_date', 'end_date', 'status', 'description'], research_projs)

    # 08 Editais de Seleção (op.admission.edital)
    editais = [
        ['edital_xyzq_cc_2024', 'Edital PPGCC 2024', 'EDITAL-PPGCC-2024', 'reg_xyzq_cc_2024', '2024', '20', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_fis_2024', 'Edital PPGFA 2024', 'EDITAL-PPGFA-2024', 'reg_xyzq_fis_2024', '2024', '20', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_bio_2024', 'Edital PPGBM 2024', 'EDITAL-PPGBM-2024', 'reg_xyzq_bio_2024', '2024', '20', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
        ['edital_xyzq_mpe_2024', 'Edital MPESI 2024', 'EDITAL-MPESI-2024', 'reg_xyzq_mpe_2024', '2024', '25', '2023-10-01', '2023-12-10', '20.0', 'homologated'],
    ]
    write_csv(os.path.join(out, "08_editais_selecao_op_admission_edital.csv"),
              ['id', 'name', 'code', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'], editais)

    # 09 a 14: Discentes, Vínculos, Planos de Trabalho, Livros-Razão, Defesas, PTT e Diplomas
    students = []
    courses_links = []
    work_plans = []
    ledger = []
    theses = []
    committees = []
    ptts = []
    ptt_authors = []
    diplomas = []
    
    prog_line_map = {
        'prog_xyzq_cc': ['line_cc_ia_01', 'line_cc_ia_02', 'line_cc_es_01', 'line_cc_es_02'],
        'prog_xyzq_fis': ['line_fis_mat_01', 'line_fis_mat_02', 'line_fis_rad_01', 'line_fis_rad_02'],
        'prog_xyzq_bio': ['line_bio_gen_01', 'line_bio_gen_02', 'line_bio_fer_01', 'line_bio_fer_02'],
        'prog_xyzq_mpe': ['line_mpe_dev_01', 'line_mpe_dev_02', 'line_mpe_gov_01', 'line_mpe_gov_02'],
    }
    
    ptt_types = [
        'l10n_br_openeducat_capes_ptt.ptt_type_t19', # Software
        'l10n_br_openeducat_capes_ptt.ptt_type_t13', # Patente
        'l10n_br_openeducat_capes_ptt.ptt_type_t07', # Protocolo Experimental
        'l10n_br_openeducat_capes_ptt.ptt_type_t09', # Manual / Guia
    ]

    stu_idx_global = 100
    for p_idx, (p_id, prog_name, short_code, _, p_modal, _, _, _, _, _) in enumerate(progs, 1):
        reg_id = f"reg_{p_id.replace('prog_', '')}_2024"
        course_id = f"crs_xyzq_{short_code.lower()[:3]}"
        if short_code == 'MPESI':
            course_id = 'crs_xyzq_mpe'
        elif short_code == 'PPGFA':
            course_id = 'crs_xyzq_fis'
        elif short_code == 'PPGBM':
            course_id = 'crs_xyzq_bio'
        elif short_code == 'PPGCC':
            course_id = 'crs_xyzq_cc'
            
        batch_id = f"batch_{course_id.replace('crs_', '')}_2024"
        n_students = 20 if p_modal == 'academic' else 25
        n_alumni = 8 if p_modal == 'academic' else 7
        subj_list = sub_lookup[p_id]
        available_fac = prog_fac_map[p_id]
        available_lines = prog_line_map[p_id]
        
        for s_idx in range(1, n_students + 1):
            stu_idx_global += 1
            g_letter = 'f' if (stu_idx_global % 2 == 0) else 'm'
            ident = gen_unique_identity(stu_idx_global, g_letter, domain="aluno.xyzq.edu.br")
            
            stu_id = f"stu_{short_code.lower()}_{s_idx:02d}"
            ra = f"RA2024{p_idx}{s_idx:03d}"
            is_alumni = (s_idx <= n_alumni)
            cat = 'alumni' if is_alumni else 'regular'
            capes_st = 'graduated' if is_alumni else 'enrolled'
            state = 'finished' if is_alumni else 'running'
            end_date = '2026-03-31' if is_alumni else ''
            
            # Orientador e Linha
            adv_id = available_fac[(s_idx - 1) % len(available_fac)]
            coadv_id = available_fac[(s_idx + 3) % len(available_fac)] if (s_idx % 4 == 0) else ''
            line_id = available_lines[(s_idx - 1) % len(available_lines)]
            
            students.append([
                stu_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
                ident['cpf'], ident['email'], ident['phone'], ra, ra, comp_id, cat, capes_st,
                'f' if g_letter == 'f' else 'm', f"{1993 + (s_idx % 7)}-08-14", '2024-03-01',
                ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
                'base.br', 'bachelor', 'grad',
                f"0000-0002-{stu_idx_global:04d}-{(stu_idx_global * 9) % 9000:04d}",
                f"http://lattes.cnpq.br/{ident['cpf']}0002",
                ident['street'], ident['city'], ident['zip'], adv_id, coadv_id, 'approved', 'not_applicable'
            ])
            
            # Vínculo com o Curso OpenEduCat
            courses_links.append([
                f"course_link_{stu_id}", stu_id, course_id, batch_id, p_id, reg_id, 'regular', state, '2024-03-01', end_date
            ])

            # Plano de Trabalho
            wp_id = f"wp_{stu_id}"
            wp_title = f"Plano de Investigação e Desenvolvimento ({short_code}): {ident['full_name']}"
            work_plans.append([
                wp_id, wp_title, stu_id, line_id, f"Linha {line_id}",
                f"Resumo da proposta de tese/dissertação do discente {ident['full_name']} no programa {short_code}.",
                "Metodologia experimental com ensaios laboratoriais e simulação computacional.",
                dummy_pdf, 'approved', 'homologated'
            ])

            # Livro-Razão Acadêmico (Append-Only)
            # Disciplinas obrigatórias (3 disciplinas)
            for code, sname, stype, creds, hrs in subj_list[:3]:
                sid = f"sub_{code.lower()}"
                ledger.append([
                    f"led_{stu_id}_{code.lower()}", stu_id, reg_id, sid, sname,
                    'subject_internal', creds, hrs, 'A' if s_idx % 2 == 0 else 'B', 'True', '2024-06-30', f"{short_code} 2024.1"
                ])

            # Disciplinas eletivas (para alumni e alunos avançados)
            if is_alumni or s_idx > 12:
                for code, sname, stype, creds, hrs in subj_list[3:6]:
                    sid = f"sub_{code.lower()}"
                    ledger.append([
                        f"led_{stu_id}_{code.lower()}", stu_id, reg_id, sid, sname,
                        'subject_internal', creds, hrs, 'A' if s_idx % 3 != 0 else 'B', 'True', '2024-12-15', f"{short_code} 2024.2"
                    ])

            if is_alumni:
                # APO / Produção Técnica
                ledger.append([f"led_{stu_id}_apo", stu_id, reg_id, '', 'Atividades Complementares e Produção Técnica', 'apo', '8', '120', 'A', 'True', '2025-11-30', 'APO'])
                # Defesa de Tese / Dissertação
                ledger.append([f"led_{stu_id}_def", stu_id, reg_id, '', 'Defesa Pública de Dissertação de Mestrado', 'milestone', '52', '780', 'A', 'True', '2026-03-31', 'Defesa'])
                
                # Defesa Homologada
                th_id = f"thesis_{stu_id}"
                th_title = f"Investigação Avançada e Inovação Tecnológica em {short_code} - Discente {ident['last_name']}"
                theses.append([th_id, stu_id, wp_id, th_title, 'dissertation', 'defense', 'homologated', '2026-03-31 14:00:00', f"http://repositorio.xyzq.edu.br/{ra.lower()}"])

                # Comissão Examinadora da Banca
                committees.append([f"comm_{th_id}_adv", th_id, adv_id, 'advisor', 'True'])
                eval_int = available_fac[(s_idx + 1) % len(available_fac)]
                eval_ext = available_fac[(s_idx + 2) % len(available_fac)]
                committees.append([f"comm_{th_id}_int", th_id, eval_int, 'internal_evaluator', 'True'])
                committees.append([f"comm_{th_id}_ext", th_id, eval_ext, 'external_evaluator', 'True'])

                # Produto PTT (para o Programa Profissional MPESI)
                if p_modal == 'professional':
                    ptt_id = f"ptt_{stu_id}"
                    chosen_ptt_type = ptt_types[s_idx % len(ptt_types)]
                    ptt_name = f"Inovação Tecnológica Aplicada MPESI ({ident['last_name']})"
                    qualis = 'T1' if s_idx % 3 == 0 else ('T2' if s_idx % 2 == 0 else 'T3')
                    trl = f"trl_{min(9, 6 + (s_idx % 4))}"
                    ptts.append([ptt_id, ptt_name, ptt_name, th_id, stu_id, chosen_ptt_type, qualis, trl, 'Aderente à Linha de Engenharia de Plataforma e Inovação', 'homologated'])
                    
                    # Coautores do PTT
                    ptt_authors.append([f"auth_{ptt_id}_stu", ptt_id, stu_id, 'main_dev', '60.0'])
                    ptt_authors.append([f"auth_{ptt_id}_adv", ptt_id, adv_id, 'advisor', '40.0'])

                # Diploma Digital com Registro Autônomo da IES
                dip_id = f"diploma_{stu_id}"
                diplomas.append([
                    dip_id, stu_id, th_id, 'master', 'autonomous_university', 'digital',
                    'Universidade XYZQ', 'Universidade XYZQ',
                    f"XYZQ-PRPG-2026-{stu_idx_global:04d}", 'LV-2026', f"{s_idx:03d}",
                    '2026-03-31', '2026-05-15', 'signed'
                ])

    write_csv(os.path.join(out, "09_discentes_identidade_op_student.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'advisor_id/id', 'coadvisor_id/id', 'english_proficiency_status', 'portuguese_proficiency_status'], students)
    
    write_csv(os.path.join(out, "10a_vinculos_curso_op_student_course.csv"),
              ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'], courses_links)

    write_csv(os.path.join(out, "10b_planos_trabalho_op_student_work_plan.csv"),
              ['id', 'name', 'student_id/id', 'research_line_id/id', 'research_line', 'summary', 'methodology', 'attachment_pdf', 'opinion_category', 'state'], work_plans)

    write_csv(os.path.join(out, "11_livro_razao_historico_op_student_credit_ledger.csv"),
              ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'], ledger)

    write_csv(os.path.join(out, "12a_bancas_defesas_capes_thesis.csv"),
              ['id', 'student_id/id', 'work_plan_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url'], theses)

    write_csv(os.path.join(out, "12b_comissoes_examinadoras_capes_thesis_committee.csv"),
              ['id', 'thesis_id/id', 'member_id/id', 'member_role', 'is_titular'], committees)

    write_csv(os.path.join(out, "13a_produtos_ptt_capes_ptt_product.csv"),
              ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'], ptts)

    write_csv(os.path.join(out, "13b_autores_ptt_capes_ptt_author.csv"),
              ['id', 'product_id/id', 'partner_id/id', 'author_role', 'ip_share'], ptt_authors)

    write_csv(os.path.join(out, "14_diplomas_digitais_capes_digital_diploma.csv"),
              ['id', 'student_id/id', 'thesis_id/id', 'degree_type', 'issuing_ies_type', 'emission_format', 'origin_ies_name', 'issuing_ies_name', 'diploma_process_number', 'registration_book_number', 'registration_page_number', 'graduation_date', 'registration_date', 'state'], diplomas)

    # 15a Comissões de Pós-Graduação (op.cpg.committee)
    cpg_committees = [
        ['cpg_xyzq_cc', 'Gestão CPG PPGCC (2024-2027)', 'prog_xyzq_cc', '2024-01-01', '2026-12-31', 'active'],
        ['cpg_xyzq_fis', 'Gestão CPG PPGFA (2024-2027)', 'prog_xyzq_fis', '2024-01-01', '2026-12-31', 'active'],
        ['cpg_xyzq_bio', 'Gestão CPG PPGBM (2024-2027)', 'prog_xyzq_bio', '2024-01-01', '2026-12-31', 'active'],
        ['cpg_xyzq_mpe', 'Gestão CPG MPESI (2024-2027)', 'prog_xyzq_mpe', '2024-01-01', '2026-12-31', 'active'],
    ]
    write_csv(os.path.join(out, "15a_governanca_cpg_comissoes_op_cpg_committee.csv"),
              ['id', 'name', 'program_id/id', 'start_date', 'end_date', 'status'], cpg_committees)

    # 15b Membros da CPG (op.cpg.member)
    cpg_members = []
    for cpg_id, p_id in [
        ('cpg_xyzq_cc', 'prog_xyzq_cc'),
        ('cpg_xyzq_fis', 'prog_xyzq_fis'),
        ('cpg_xyzq_bio', 'prog_xyzq_bio'),
        ('cpg_xyzq_mpe', 'prog_xyzq_mpe'),
    ]:
        f_pool = prog_fac_map[p_id]
        cpg_members.append([f"mem_{cpg_id}_coord", cpg_id, f_pool[0], 'coordinator', 'peer_election', f"Portaria CPG-XYZQ 01/{cpg_id[-2:]}"])
        cpg_members.append([f"mem_{cpg_id}_vice", cpg_id, f_pool[1], 'vice_coordinator', 'peer_election', f"Portaria CPG-XYZQ 02/{cpg_id[-2:]}"])
        cpg_members.append([f"mem_{cpg_id}_tit1", cpg_id, f_pool[2], 'titular', 'peer_election', f"Portaria CPG-XYZQ 03/{cpg_id[-2:]}"])
        cpg_members.append([f"mem_{cpg_id}_tit2", cpg_id, f_pool[3], 'titular', 'peer_election', f"Portaria CPG-XYZQ 04/{cpg_id[-2:]}"])
        cpg_members.append([f"mem_{cpg_id}_sup1", cpg_id, f_pool[4], 'suplente', 'peer_election', f"Portaria CPG-XYZQ 05/{cpg_id[-2:]}"])
        cpg_members.append([f"mem_{cpg_id}_sup2", cpg_id, f_pool[5], 'suplente', 'peer_election', f"Portaria CPG-XYZQ 06/{cpg_id[-2:]}"])

    write_csv(os.path.join(out, "15b_membros_cpg_op_cpg_member.csv"),
              ['id', 'committee_id/id', 'partner_id/id', 'role', 'mandate_origin', 'document_ref'], cpg_members)

    # 15c Reuniões Ordinárias da CPG (op.cpg.meeting)
    cpg_meetings = []
    for cpg_id, _ in [('cpg_xyzq_cc', 'prog_xyzq_cc'), ('cpg_xyzq_mpe', 'prog_xyzq_mpe')]:
        for month in range(2, 10):
            m_id = f"meet_{cpg_id}_2024_{month:02d}"
            m_name = f"{month-1}ª Reunião Ordinária da CPG ({cpg_id.replace('cpg_xyzq_', '').upper()} 2024)"
            cpg_meetings.append([m_id, m_name, cpg_id, f"2024-{month:02d}-15 14:00:00", 'ordinary', 'published'])
    write_csv(os.path.join(out, "15c_reunioes_atas_cpg_op_cpg_meeting.csv"),
              ['id', 'name', 'committee_id/id', 'meeting_date', 'meeting_type', 'state'], cpg_meetings)

    # 16 Perfis de Usuários (res.users)
    users = [
        ['user_xyzq_admin', 'Administrador Geral XYZQ', 'admin_xyzq', 'admin.posgrad@xyzq.edu.br', comp_id],
        ['user_xyzq_sec', 'Secretaria Central de Pós-Graduação', 'secretaria_xyzq', 'sec.posgrad@xyzq.edu.br', comp_id],
        ['user_xyzq_coord_cc', 'Coordenador PPGCC (Prof. Carlos)', 'coord_ppgcc', 'coord.ppgcc@xyzq.edu.br', comp_id],
        ['user_xyzq_coord_mpe', 'Coordenador MPESI (Prof. Eduardo)', 'coord_mpesi', 'coord.mpesi@xyzq.edu.br', comp_id],
        ['user_xyzq_prof', 'Docente Permanente PPG (Prof. Roberto)', 'prof_xyzq', 'roberto.docente@xyzq.edu.br', comp_id],
    ]
    write_csv(os.path.join(out, "16_usuarios_perfis_res_users.csv"),
              ['id', 'name', 'login', 'email', 'company_id/id'], users)


# ------------------------------------------------------------------------------
# SCENARIO 2: MPTRCS / IPEN-CNEN/SP
# ------------------------------------------------------------------------------
def generate_scenario_mptrcs(base_dir):
    print("--- Generating Scenario 2: MPTRCS / IPEN-CNEN/SP ---")
    out = os.path.join(base_dir, "mptrcs_ipen")
    comp_id = "comp_ies_ipen"
    p_id = "prog_mptrcs"
    reg_id = "reg_mptrcs_v2"
    dummy_pdf = base64.b64encode(b"%PDF-1.4 Mock Plano de Trabalho MPTRCS").decode('utf-8')
    
    # 01a Company
    write_csv(os.path.join(out, "01a_ies_instituicao_res_company.csv"),
              ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
              [[comp_id, 'Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP', '00.394.429/0001-00', '1902', 'Av. Prof. Lineu Prestes, 2242 - Cidade Universitária', 'São Paulo', '05508-000', 'BR']])

    # 01b Departamentos OpenEduCat (op.department)
    depts = [
        ['dept_ipen_ctr', 'Centro de Tecnologia das Radiações (CTR)', 'CTR-IPEN'],
        ['dept_ipen_cpg', 'Comissão de Pós-Graduação (CPG-IPEN)', 'CPG-IPEN'],
        ['dept_ipen_sec', 'Secretaria de Pós-Graduação (SECPG)', 'SECPG-IPEN'],
    ]
    write_csv(os.path.join(out, "01b_departamentos_op_department.csv"),
              ['id', 'name', 'code'], depts)

    # 01c Categorias OpenEduCat (op.category)
    cats = [
        ['cat_ipen_reg', 'Aluno Regular MPTRCS', 'REG-MPTRCS', comp_id],
        ['cat_ipen_esp', 'Aluno Especial / Avulso', 'ESP-MPTRCS', comp_id],
        ['cat_ipen_doc_perm', 'Docente Permanente CPG', 'DOC-PERM', comp_id],
        ['cat_ipen_doc_colab', 'Docente Colaborador', 'DOC-COLAB', comp_id],
        ['cat_ipen_rep_disc', 'Representante Discente CPG', 'REP-DISC', comp_id],
    ]
    write_csv(os.path.join(out, "01c_categorias_op_category.csv"),
              ['id', 'name', 'code', 'company_id/id'], cats)

    # 01d Anos Acadêmicos (op.academic.year)
    years = []
    for y in range(2022, 2027):
        years.append([f"ay_ipen_{y}", f"Ano Acadêmico {y}", f"{y}-01-01", f"{y}-12-31", 'two_sem', comp_id])
    write_csv(os.path.join(out, "01d_anos_academicos_op_academic_year.csv"),
              ['id', 'name', 'start_date', 'end_date', 'term_structure', 'company_id/id'], years)

    # 01e Termos Letivos / Semestres (op.academic.term)
    terms = []
    for y in range(2022, 2027):
        terms.append([f"term_ipen_{y}_1", f"{y}.1", f"ay_ipen_{y}", f"{y}-02-01", f"{y}-06-30", comp_id])
        terms.append([f"term_ipen_{y}_2", f"{y}.2", f"ay_ipen_{y}", f"{y}-08-01", f"{y}-12-15", comp_id])
    write_csv(os.path.join(out, "01e_termos_academicos_op_academic_term.csv"),
              ['id', 'name', 'academic_year_id/id', 'term_start_date', 'term_end_date', 'company_id/id'], terms)

    # 01f Níveis de Programa (op.program.level)
    levels = [
        ['level_ipen_prof', 'Pós-Graduação Stricto Sensu - Mestrado Profissional'],
    ]
    write_csv(os.path.join(out, "01f_niveis_programa_op_program_level.csv"),
              ['id', 'name'], levels)

    # 01g Programas OpenEduCat (op.program)
    oe_progs = [
        ['prog_oe_mptrcs', 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde', 'MPTRCS', 'level_ipen_prof', 'dept_ipen_ctr', 'True'],
    ]
    write_csv(os.path.join(out, "01g_programas_openeducat_op_program.csv"),
              ['id', 'name', 'code', 'program_level_id/id', 'department_id/id', 'active'], oe_progs)

    # 01h Cursos OpenEduCat (op.course)
    courses = [
        ['crs_ipen_mptrcs', 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde', 'MPTRCS', 'normal', 'prog_oe_mptrcs', 'dept_ipen_ctr'],
    ]
    write_csv(os.path.join(out, "01h_cursos_openeducat_op_course.csv"),
              ['id', 'name', 'code', 'evaluation_type', 'program_id/id', 'department_id/id'], courses)

    # 01i Lotes / Turmas (op.batch)
    batches = [
        ['batch_ipen_t1', 'Turma 1 (2022)', 'MPTRCS-T1', 'crs_ipen_mptrcs', '2022-03-01', '2024-04-30', 'True'],
        ['batch_ipen_t2', 'Turma 2 (2023)', 'MPTRCS-T2', 'crs_ipen_mptrcs', '2023-03-01', '2025-04-30', 'True'],
        ['batch_ipen_t3', 'Turma 3 (2024)', 'MPTRCS-T3', 'crs_ipen_mptrcs', '2024-03-01', '2026-04-30', 'True'],
        ['batch_ipen_t4', 'Turma 4 (2025)', 'MPTRCS-T4', 'crs_ipen_mptrcs', '2025-03-01', '2027-04-30', 'True'],
    ]
    write_csv(os.path.join(out, "01i_lotes_turmas_op_batch.csv"),
              ['id', 'name', 'code', 'course_id/id', 'start_date', 'end_date', 'active'], batches)

    # 02 Programas CAPES (op.program.capes)
    write_csv(os.path.join(out, "02_programas_capes_op_program.csv"),
              ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id', 'evaluation_area', 'status'],
              [[p_id, 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde', 'MPTRCS', '33002010001P0', 'professional', '4', 'semestral', comp_id, 'Medicina III / Física Médica', 'active']])

    # 03 Versão Curricular (op.curriculum.version)
    write_csv(os.path.join(out, "03_versao_curricular_op_curriculum_version.csv"),
              ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'],
              [[reg_id, 'Regulamento MP-TRCS v2 (2024)', p_id, '100', '40', '52', '8', '15', '50', '24', 'False', '0', '36', 'cpg_approval', 'omit_on_regular', 'False', '0', 'True', 'current_matrix', 'scale_abc_r', 'admission', 'not_applicable', 'cpg_checklist', 'hybrid_allowed']])

    # 04a Áreas de Concentração (op.program.concentration.area)
    areas = [
        ['area_rad_dos', 'Radioterapia e Dosimetria das Radiações', 'RAD-DOS', p_id, 'Física médica, dosimetria e controle de qualidade em radioterapia'],
        ['area_rad_nuc', 'Medicina Nuclear e Radiofarmácia', 'RAD-NUC', p_id, 'Radiofármacos inovadores, imunologia molecular e dosimetria interna'],
    ]
    write_csv(os.path.join(out, "04a_areas_concentracao_op_program_concentration_area.csv"),
              ['id', 'name', 'code', 'program_id/id', 'description'], areas)

    # 04b Linhas de Pesquisa (op.program.research.line)
    lines = [
        ['line_rad_dos_01', 'Dosimetria Clínica e Planejamento Radioterápico Avançado', 'RAD-DOS-01', 'area_rad_dos', 'Desenvolvimento de protocolos dosimétricos e simulação Monte Carlo'],
        ['line_rad_dos_02', 'Controle da Qualidade e Segurança em Feixes de Radiação Ionizante', 'RAD-DOS-02', 'area_rad_dos', 'Desenvolvimento de dispositivos e fantomas de garantia da qualidade'],
        ['line_rad_nuc_01', 'Desenvolvimento e Caracterização de Radiofármacos Diagnósticos e Terapêuticos', 'RAD-NUC-01', 'area_rad_nuc', 'Síntese, controle biológico e ensaios pré-clínicos de radiofármacos'],
        ['line_rad_nuc_02', 'Instrumentação Nuclear, Dosimetria Interna e Imagens Moleculares', 'RAD-NUC-02', 'area_rad_nuc', 'Reconstrução tomográfica PET/SPECT e dosimetria interna personalizada'],
    ]
    write_csv(os.path.join(out, "04b_linhas_pesquisa_op_program_research_line.csv"),
              ['id', 'name', 'code', 'area_id/id', 'description'], lines)

    # 05 Docentes Orientadores (op.faculty) — 12 professores únicos
    fac_records = []
    link_records = []
    ledger_records = []
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
        link_id = f"link_{fac_id}_{p_id}"
        link_records.append([link_id, fac_id, p_id])
        ledger_records.append([
            f"fac_led_mptrcs_{f_idx:02d}", link_id, 'permanent', '2021-01-01', '',
            f"Portaria DIR-IPEN {f_idx:03d}/2021", 'Credenciamento Permanente CPG'
        ])

    write_csv(os.path.join(out, "05_docentes_orientadores_op_faculty.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'gender', 'birth_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'work_regime', 'workload', 'degree_level', 'degree_area', 'degree_ies', 'orcid', 'lattes_url', 'street', 'city', 'zip'], fac_records)
    write_csv(os.path.join(out, "06a_vinculos_docente_programa_op_faculty_program_link.csv"),
              ['id', 'faculty_id/id', 'program_id/id'], link_records)
    write_csv(os.path.join(out, "06b_credenciamento_docente_ledger_op_faculty_category_ledger.csv"),
              ['id', 'program_link_id/id', 'category', 'start_date', 'end_date', 'document_ref', 'notes'], ledger_records)

    # 07a Disciplinas do Catálogo (op.subject)
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
    write_csv(os.path.join(out, "07a_disciplinas_catalogo_op_subject.csv"),
              ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'], subjects)

    rules = []
    for sid, sname, code, _, stype, _, _ in subjects:
        rules.append([f"rule_{sid}", reg_id, sid, 'Radioterapia / Medicina Nuclear', 'program' if stype == 'compulsory' else 'area'])
    write_csv(os.path.join(out, "07b_regras_curriculares_op_curriculum_subject_rule.csv"),
              ['id', 'curriculum_version_id/id', 'subject_id/id', 'area_name', 'scope'], rules)

    # 07c Projetos de Pesquisa Institucionais
    proj_data = [
        ['proj_mptrcs_01', 'Desenvolvimento de Fantomas e Sensores para Dosimetria 3D em Radioterapia', p_id, fac_ids[0], 'line_rad_dos_01', 'applied', 'FAPESP', '2021/14589-2', '2021-03-01', '2026-12-31', 'ongoing', 'Fantomas e dosimetria 3D'],
        ['proj_mptrcs_02', 'Controle de Qualidade Automatizado em Aceleradores Médicos Lineares', p_id, fac_ids[1], 'line_rad_dos_02', 'applied', 'CNPq', '408120/2021-8', '2021-03-01', '2026-12-31', 'ongoing', 'Automação de CQ em radioterapia'],
        ['proj_mptrcs_03', 'Síntese e Avaliação Biológica de Radiofármacos Marcados com Lutécio-177', p_id, fac_ids[4], 'line_rad_nuc_01', 'applied', 'CNEN', '01300.0012/2022', '2022-03-01', '2026-12-31', 'ongoing', 'Radiofármacos inovadores Lu-177'],
        ['proj_mptrcs_04', 'Quantificação e Reconstrução de Imagens Moleculares em PET/CT', p_id, fac_ids[5], 'line_rad_nuc_02', 'applied', 'IAEA', 'BRA/6/029', '2021-03-01', '2026-12-31', 'ongoing', 'Processamento tomográfico PET/SPECT'],
    ]
    write_csv(os.path.join(out, "07c_projetos_pesquisa_capes_research_project.csv"),
              ['id', 'name', 'program_id/id', 'coordinator_id/id', 'research_line_id/id', 'research_nature', 'funding_agency', 'funding_process', 'start_date', 'end_date', 'status', 'description'], proj_data)

    # 08 Editais
    editais = [
        ['edital_mptrcs_t1', 'Edital Processo Seletivo MPTRCS - Turma 1 (2022)', 'EDITAL-MPTRCS-2022', reg_id, '2022', '15', '2021-10-01', '2021-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t2', 'Edital Processo Seletivo MPTRCS - Turma 2 (2023)', 'EDITAL-MPTRCS-2023', reg_id, '2023', '15', '2022-10-01', '2022-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t3', 'Edital Processo Seletivo MPTRCS - Turma 3 (2024)', 'EDITAL-MPTRCS-2024', reg_id, '2024', '15', '2023-10-01', '2023-12-15', '20.0', 'homologated'],
        ['edital_mptrcs_t4', 'Edital Processo Seletivo MPTRCS - Turma 4 (2025)', 'EDITAL-MPTRCS-2025', reg_id, '2025', '15', '2024-10-01', '2024-12-15', '20.0', 'published'],
    ]
    write_csv(os.path.join(out, "08_editais_selecao_op_admission_edital.csv"),
              ['id', 'name', 'code', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'], editais)

    # 09 a 14: Discentes MPTRCS
    students = []
    courses_links = []
    work_plans = []
    ledger = []
    theses = []
    committees = []
    ptts = []
    ptt_authors = []
    diplomas = []

    t_cfg = [
        (1, 2022, 15, 0),
        (2, 2023, 15, 0),
        (3, 2024, 12, 3),
        (4, 2025, 0, 15),
    ]

    all_lines = ['line_rad_dos_01', 'line_rad_dos_02', 'line_rad_nuc_01', 'line_rad_nuc_02']
    ptt_types = [
        'l10n_br_openeducat_capes_ptt.ptt_type_t19',
        'l10n_br_openeducat_capes_ptt.ptt_type_t07',
        'l10n_br_openeducat_capes_ptt.ptt_type_t09',
        'l10n_br_openeducat_capes_ptt.ptt_type_t13',
    ]

    mptrcs_stu_counter = 0
    for t_num, year, n_tit, n_cur in t_cfg:
        batch_id = f"batch_ipen_t{t_num}"
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

            adv_id = fac_ids[(mptrcs_stu_counter - 1) % len(fac_ids)]
            coadv_id = fac_ids[(mptrcs_stu_counter + 3) % len(fac_ids)] if (mptrcs_stu_counter % 4 == 0) else ''
            line_id = all_lines[(mptrcs_stu_counter - 1) % len(all_lines)]

            students.append([
                stu_id, ident['full_name'], ident['first_name'], ident['middle_name'], ident['last_name'],
                ident['cpf'], ident['email'], ident['phone'], ra, ra, comp_id, cat, capes_st,
                'f' if g_letter == 'f' else 'm', f"{b_year}-07-22", f"{year}-03-01",
                ident['mother_name'], ident['race'], ident['has_disability'], ident['city'], ident['state_abbr'],
                'base.br', 'bachelor', 'grad',
                f"0000-0002-{mptrcs_stu_counter + 4000:04d}-{(mptrcs_stu_counter * 13) % 9000:04d}",
                f"http://lattes.cnpq.br/{ident['cpf']}0002",
                ident['street'], ident['city'], ident['zip'], adv_id, coadv_id, 'approved', 'not_applicable'
            ])

            courses_links.append([
                f"link_{stu_id}", stu_id, 'crs_ipen_mptrcs', batch_id, p_id, reg_id, 'regular', state, f"{year}-03-01", end_date
            ])

            wp_id = f"wp_{stu_id}"
            wp_title = f"Plano de Investigação e Desenvolvimento Tecnológico: {ident['full_name']}"
            work_plans.append([
                wp_id, wp_title, stu_id, line_id, f"Linha {line_id}",
                f"Desenvolvimento de tecnologia radiológica no âmbito do MPTRCS. Investigação discente {ident['full_name']}.",
                "Ensaios laboratoriais e dosimétricos com feixes clínicos e modelagem computacional.",
                dummy_pdf, 'approved', 'homologated'
            ])

            # Livro-Razão
            for sid, sname, code, _, _, _, creds in subjects[:3]:
                ledger.append([
                    f"led_{stu_id}_{code.lower()}", stu_id, reg_id, sid, sname,
                    'subject_internal', creds, creds * 15, 'A' if s_idx % 2 == 0 else 'B', 'True', f"{year}-06-30", f"Turma {t_num} Sem 1"
                ])

            if is_alumni or t_num == 3:
                for sid, sname, code, _, _, _, creds in subjects[3:]:
                    ledger.append([
                        f"led_{stu_id}_{code.lower()}", stu_id, reg_id, sid, sname,
                        'subject_internal', creds, creds * 15, 'A' if s_idx % 3 != 0 else 'B', 'True', f"{year}-12-15", f"Turma {t_num} Sem 2"
                    ])

            if is_alumni:
                ledger.append([f"led_{stu_id}_apo", stu_id, reg_id, '', 'Seminários de Acompanhamento e Desenvolvimento de PTT', 'apo', '8', '120', 'A', 'True', f"{year+1}-11-30", f"Turma {t_num} APO"])
                ledger.append([f"led_{stu_id}_def", stu_id, reg_id, '', 'Defesa Pública de Dissertação e Produto Tecnológico', 'milestone', '52', '780', 'A', 'True', f"{year+2}-04-15", f"Turma {t_num} Defesa"])

                th_id = f"thesis_{stu_id}"
                th_title = f"Otimização Dosimétrica e Inovação Tecnológica em Feixes Clínicos - Estudo {ident['last_name']}"
                theses.append([th_id, stu_id, wp_id, th_title, 'dissertation', 'defense', 'homologated', f"{year+2}-04-15 14:00:00", f"http://repositorio.ipen.br/handle/123456789/{mptrcs_stu_counter}"])

                eval_int = fac_ids[(mptrcs_stu_counter + 1) % len(fac_ids)]
                eval_ext = fac_ids[(mptrcs_stu_counter + 2) % len(fac_ids)]
                committees.append([f"comm_{th_id}_adv", th_id, adv_id, 'advisor', 'True'])
                committees.append([f"comm_{th_id}_int", th_id, eval_int, 'internal_evaluator', 'True'])
                committees.append([f"comm_{th_id}_ext", th_id, eval_ext, 'external_evaluator', 'True'])

                ptt_id = f"ptt_{stu_id}"
                chosen_ptt_type = ptt_types[(s_idx + t_num) % len(ptt_types)]
                ptt_name = f"Inovação Tecnológica Aplicada MPTRCS: Software Dosimétrico ({ident['last_name']})"
                qualis = 'T1' if s_idx % 3 == 0 else ('T2' if s_idx % 2 == 0 else 'T3')
                trl = f"trl_{min(9, 6 + (s_idx % 4))}"
                ptts.append([ptt_id, ptt_name, ptt_name, th_id, stu_id, chosen_ptt_type, qualis, trl, 'Aderente à Linha de Radioterapia e Dosimetria', 'homologated'])
                
                ptt_authors.append([f"auth_{ptt_id}_stu", ptt_id, stu_id, 'main_dev', '60.0'])
                ptt_authors.append([f"auth_{ptt_id}_adv", ptt_id, adv_id, 'advisor', '40.0'])

                dip_id = f"diploma_{stu_id}"
                diplomas.append([
                    dip_id, stu_id, th_id, 'master', 'external_registering_university', 'digital',
                    'Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP', 'Universidade de São Paulo - USP',
                    f"USP-PRPG-{year+2}-{mptrcs_stu_counter:04d}", f"LV-{year+2}", f"{s_idx:03d}",
                    f"{year+2}-04-15", f"{year+2}-06-20", 'signed'
                ])

    write_csv(os.path.join(out, "09_discentes_identidade_op_student.csv"),
              ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'advisor_id/id', 'coadvisor_id/id', 'english_proficiency_status', 'portuguese_proficiency_status'], students)

    write_csv(os.path.join(out, "10a_vinculos_curso_op_student_course.csv"),
              ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'], courses_links)

    write_csv(os.path.join(out, "10b_planos_trabalho_op_student_work_plan.csv"),
              ['id', 'name', 'student_id/id', 'research_line_id/id', 'research_line', 'summary', 'methodology', 'attachment_pdf', 'opinion_category', 'state'], work_plans)

    write_csv(os.path.join(out, "11_livro_razao_historico_op_student_credit_ledger.csv"),
              ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'], ledger)

    write_csv(os.path.join(out, "12a_bancas_defesas_capes_thesis.csv"),
              ['id', 'student_id/id', 'work_plan_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url'], theses)

    write_csv(os.path.join(out, "12b_comissoes_examinadoras_capes_thesis_committee.csv"),
              ['id', 'thesis_id/id', 'member_id/id', 'member_role', 'is_titular'], committees)

    write_csv(os.path.join(out, "13a_produtos_ptt_capes_ptt_product.csv"),
              ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'], ptts)

    write_csv(os.path.join(out, "13b_autores_ptt_capes_ptt_author.csv"),
              ['id', 'product_id/id', 'partner_id/id', 'author_role', 'ip_share'], ptt_authors)

    write_csv(os.path.join(out, "14_diplomas_digitais_capes_digital_diploma.csv"),
              ['id', 'student_id/id', 'thesis_id/id', 'degree_type', 'issuing_ies_type', 'emission_format', 'origin_ies_name', 'issuing_ies_name', 'diploma_process_number', 'registration_book_number', 'registration_page_number', 'graduation_date', 'registration_date', 'state'], diplomas)

    # 15 CPG Governance
    cpg_committees = [
        ['cpg_mptrcs_2022', 'Gestão CPG MPTRCS (2022-2025)', p_id, '2022-01-01', '2024-12-31', 'closed'],
        ['cpg_mptrcs_2025', 'Gestão CPG MPTRCS (2025-2028)', p_id, '2025-01-01', '2027-12-31', 'active'],
    ]
    write_csv(os.path.join(out, "15a_governanca_cpg_comissoes_op_cpg_committee.csv"),
              ['id', 'name', 'program_id/id', 'start_date', 'end_date', 'status'], cpg_committees)

    cpg_members = [
        ['mem_mptrcs_coord', 'cpg_mptrcs_2025', fac_ids[0], 'coordinator', 'peer_election', 'Portaria DIR-IPEN 001/2025'],
        ['mem_mptrcs_vice', 'cpg_mptrcs_2025', fac_ids[1], 'vice_coordinator', 'peer_election', 'Portaria DIR-IPEN 002/2025'],
        ['mem_mptrcs_tit1', 'cpg_mptrcs_2025', fac_ids[2], 'titular', 'peer_election', 'Portaria DIR-IPEN 003/2025'],
        ['mem_mptrcs_tit2', 'cpg_mptrcs_2025', fac_ids[3], 'titular', 'peer_election', 'Portaria DIR-IPEN 004/2025'],
        ['mem_mptrcs_sup1', 'cpg_mptrcs_2025', fac_ids[4], 'suplente', 'peer_election', 'Portaria DIR-IPEN 005/2025'],
        ['mem_mptrcs_sup2', 'cpg_mptrcs_2025', fac_ids[5], 'suplente', 'peer_election', 'Portaria DIR-IPEN 006/2025'],
    ]
    write_csv(os.path.join(out, "15b_membros_cpg_op_cpg_member.csv"),
              ['id', 'committee_id/id', 'partner_id/id', 'role', 'mandate_origin', 'document_ref'], cpg_members)

    cpg_meetings = []
    for month in range(2, 10):
        m_id = f"meet_mptrcs_2026_{month:02d}"
        m_name = f"{month-1}ª Reunião Ordinária da CPG MPTRCS (2026)"
        cpg_meetings.append([m_id, m_name, 'cpg_mptrcs_2025', f"2026-{month:02d}-15 14:00:00", 'ordinary', 'published'])
    write_csv(os.path.join(out, "15c_reunioes_atas_cpg_op_cpg_meeting.csv"),
              ['id', 'name', 'committee_id/id', 'meeting_date', 'meeting_type', 'state'], cpg_meetings)

    # 16 Usuários
    users = [
        ['user_mptrcs_admin', 'Administrador MPTRCS', 'admin_mptrcs', 'admin@ipen.br', comp_id],
        ['user_mptrcs_sec', 'Secretaria MPTRCS', 'secretaria_mptrcs', 'secretaria.mptrcs@ipen.br', comp_id],
        ['user_mptrcs_coord', 'Coordenador MPTRCS', 'coord_mptrcs', 'coordenacao.mptrcs@ipen.br', comp_id],
        ['user_mptrcs_prof', 'Professor MPTRCS', 'prof_mptrcs', 'professor.mptrcs@ipen.br', comp_id],
    ]
    write_csv(os.path.join(out, "16_usuarios_perfis_res_users.csv"),
              ['id', 'name', 'login', 'email', 'company_id/id'], users)


# ------------------------------------------------------------------------------
# STANDARDIZED SKELETON TEMPLATES
# ------------------------------------------------------------------------------
def generate_standard_skeletons(base_dir):
    print("--- Generating Standardized Skeletons ---")
    out = os.path.join(base_dir, "esqueletos_padronizados")
    
    skeletons = {
        "01a_ies_instituicao_res_company.csv": ['id', 'name', 'cnpj', 'emec_code', 'street', 'city', 'zip', 'country_id/code'],
        "01b_departamentos_op_department.csv": ['id', 'name', 'code'],
        "01c_categorias_op_category.csv": ['id', 'name', 'code', 'company_id/id'],
        "01d_anos_academicos_op_academic_year.csv": ['id', 'name', 'start_date', 'end_date', 'term_structure', 'company_id/id'],
        "01e_termos_academicos_op_academic_term.csv": ['id', 'name', 'academic_year_id/id', 'term_start_date', 'term_end_date', 'company_id/id'],
        "01f_niveis_programa_op_program_level.csv": ['id', 'name'],
        "01g_programas_openeducat_op_program.csv": ['id', 'name', 'code', 'program_level_id/id', 'department_id/id', 'active'],
        "01h_cursos_openeducat_op_course.csv": ['id', 'name', 'code', 'evaluation_type', 'program_id/id', 'department_id/id'],
        "01i_lotes_turmas_op_batch.csv": ['id', 'name', 'code', 'course_id/id', 'start_date', 'end_date', 'active'],
        "02_programas_capes_op_program.csv": ['id', 'name', 'short_name', 'snpg_code', 'modality', 'capes_grade', 'school_term', 'company_id/id', 'evaluation_area', 'status'],
        "03_versao_curricular_op_curriculum_version.csv": ['id', 'name', 'program_id/id', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'credit_hour_ratio', 'max_external_credits_percent', 'max_months_defense', 'allow_special_students', 'max_special_subjects_limit', 'special_credit_validity_months', 'special_incorporation_workflow', 'special_transcript_fail_policy', 'allow_intra_ies_credits', 'max_intra_ies_credits_percent', 'intra_ies_advisor_approval_required', 'retorno_rule', 'grading_scale_type', 'proficiency_stage', 'teaching_internship_mode', 'ptt_validation_mode', 'defense_location_policy'],
        "04a_areas_concentracao_op_program_concentration_area.csv": ['id', 'name', 'code', 'program_id/id', 'description'],
        "04b_linhas_pesquisa_op_program_research_line.csv": ['id', 'name', 'code', 'area_id/id', 'description'],
        "05_docentes_orientadores_op_faculty.csv": ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'gender', 'birth_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'work_regime', 'workload', 'degree_level', 'degree_area', 'degree_ies', 'orcid', 'lattes_url', 'street', 'city', 'zip'],
        "06a_vinculos_docente_programa_op_faculty_program_link.csv": ['id', 'faculty_id/id', 'program_id/id'],
        "06b_credenciamento_docente_ledger_op_faculty_category_ledger.csv": ['id', 'program_link_id/id', 'category', 'start_date', 'end_date', 'document_ref', 'notes'],
        "07a_disciplinas_catalogo_op_subject.csv": ['id', 'name', 'code', 'type', 'subject_type', 'program_id/id', 'grade_weightage'],
        "07b_regras_curriculares_op_curriculum_subject_rule.csv": ['id', 'curriculum_version_id/id', 'subject_id/id', 'area_name', 'scope'],
        "07c_projetos_pesquisa_capes_research_project.csv": ['id', 'name', 'program_id/id', 'coordinator_id/id', 'research_line_id/id', 'research_nature', 'funding_agency', 'funding_process', 'start_date', 'end_date', 'status', 'description'],
        "08_editais_selecao_op_admission_edital.csv": ['id', 'name', 'code', 'curriculum_version_id/id', 'academic_year', 'total_slots', 'start_date', 'end_date', 'affirmative_action_percent', 'state'],
        "09_discentes_identidade_op_student.csv": ['id', 'name', 'first_name', 'middle_name', 'last_name', 'cpf', 'email', 'phone', 'ra_number', 'gr_no', 'company_id/id', 'student_category', 'capes_status', 'gender', 'birth_date', 'admission_date', 'mother_name', 'race_color', 'has_disability', 'birth_city_name', 'birth_state', 'nationality/id', 'highest_degree', 'academic_level', 'orcid', 'lattes_url', 'street', 'city', 'zip', 'advisor_id/id', 'coadvisor_id/id', 'english_proficiency_status', 'portuguese_proficiency_status'],
        "10a_vinculos_curso_op_student_course.csv": ['id', 'student_id/id', 'course_id/id', 'batch_id/id', 'program_id/id', 'curriculum_version_id/id', 'course_type', 'state', 'admission_date', 'completion_date'],
        "10b_planos_trabalho_op_student_work_plan.csv": ['id', 'name', 'student_id/id', 'research_line_id/id', 'research_line', 'summary', 'methodology', 'attachment_pdf', 'opinion_category', 'state'],
        "11_livro_razao_historico_op_student_credit_ledger.csv": ['id', 'student_id/id', 'curriculum_version_id/id', 'subject_id/id', 'course_name', 'credit_type', 'credits', 'hours', 'grade_concept', 'is_approved', 'date_earned', 'origin_ref'],
        "12a_bancas_defesas_capes_thesis.csv": ['id', 'student_id/id', 'work_plan_id/id', 'title', 'doc_type', 'stage', 'status', 'defense_date', 'repository_url'],
        "12b_comissoes_examinadoras_capes_thesis_committee.csv": ['id', 'thesis_id/id', 'member_id/id', 'member_role', 'is_titular'],
        "13a_produtos_ptt_capes_ptt_product.csv": ['id', 'title', 'name', 'thesis_id/id', 'student_id/id', 'type_id/id', 'final_stratum', 'trl_level', 'adherence_justif', 'state'],
        "13b_autores_ptt_capes_ptt_author.csv": ['id', 'product_id/id', 'partner_id/id', 'author_role', 'ip_share'],
        "14_diplomas_digitais_capes_digital_diploma.csv": ['id', 'student_id/id', 'thesis_id/id', 'degree_type', 'issuing_ies_type', 'emission_format', 'origin_ies_name', 'issuing_ies_name', 'diploma_process_number', 'registration_book_number', 'registration_page_number', 'graduation_date', 'registration_date', 'state'],
        "15a_governanca_cpg_comissoes_op_cpg_committee.csv": ['id', 'name', 'program_id/id', 'start_date', 'end_date', 'status'],
        "15b_membros_cpg_op_cpg_member.csv": ['id', 'committee_id/id', 'partner_id/id', 'role', 'mandate_origin', 'document_ref'],
        "15c_reunioes_atas_cpg_op_cpg_meeting.csv": ['id', 'name', 'committee_id/id', 'meeting_date', 'meeting_type', 'state'],
        "16_usuarios_perfis_res_users.csv": ['id', 'name', 'login', 'email', 'company_id/id'],
    }
    
    for filename, headers in skeletons.items():
        write_csv(os.path.join(out, filename), headers, [])


if __name__ == '__main__':
    base_dir = 'import_templates'
    generate_scenario_xyzq(os.path.join(base_dir, 'datasets_sinteticos'))
    generate_scenario_mptrcs(os.path.join(base_dir, 'datasets_sinteticos'))
    generate_standard_skeletons(base_dir)
    print('[SUCCESS] All synthetic datasets and skeletons regenerated with 100% compliant schemas and unique names!')
