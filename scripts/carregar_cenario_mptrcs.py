#!/usr/bin/env python3
"""
Carregador Completo do Cenário MPTRCS no Odoo 19 (Banco mptrcs_ipen_prod)
Executa via API ORM do Odoo, com:
1. Áreas de Concentração e Linhas de Pesquisa
2. 12 Docentes com nomes únicos, separação first/middle/last, censo CAPES completo e vínculos temáticos
3. 4 Projetos de Pesquisa coordenados por docentes com fomento oficial
4. 60 Discentes (Turmas 1 a 4) com NOMES 100% ÚNICOS (sem repetição e sem sufixos),
   dados censitários CAPES completos (mãe, raça/cor, deficiência, naturalidade, endereço, PIDs),
   vínculos de curso, planos de trabalho vinculados a linhas, livro-razão de créditos,
   ritos de defesa com comissões examinadoras completas, produtos PTT com coautoria docente,
   e diplomas digitais com registro externo USP.
"""
import os
import sys
import base64
import random
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

DB_NAME = 'mptrcs_ipen_prod'
CONFIG_PATH = '/etc/odoo/odoo.conf'

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

used_full_names = set()

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

def gen_unique_identity(idx, gender_letter, is_faculty=False):
    """Gera uma pessoa brasileira completa e com nome 100% único garantido."""
    first_pool = MALE_FIRST if gender_letter == 'm' else FEMALE_FIRST
    first = first_pool[idx % len(first_pool)]
    
    # Busca combinação única de middle e last
    attempts = 0
    while True:
        mid = MIDDLES[(idx * 7 + attempts * 13) % len(MIDDLES)]
        last = LASTS[(idx * 11 + attempts * 17) % len(LASTS)]
        full_name = f"{first} {mid} {last}"
        if full_name not in used_full_names:
            used_full_names.add(full_name)
            break
        attempts += 1
    
    cpf = gen_cpf(idx + 1000)
    
    m_first = MOTHER_FIRSTS[(idx * 3) % len(MOTHER_FIRSTS)]
    m_conn = MOTHER_CONNECTORS[(idx * 5) % len(MOTHER_CONNECTORS)]
    mother_name = f"{m_first} {m_conn} {last}"
    
    city, state_abbr = CITIES[idx % len(CITIES)]
    street = f"{STREETS[idx % len(STREETS)]}, {100 + (idx * 15) % 900}"
    street2 = f"Apto {(idx % 18) + 1}02" if idx % 2 == 0 else ""
    zip_code = f"0{1000 + (idx * 37) % 8900:04d}-{(idx * 19) % 890:03d}"
    phone = f"(11) 9{8000 + (idx * 23) % 1900:04d}-{(idx * 31) % 9000:04d}"
    
    race = RACES[idx % len(RACES)]
    has_disability = (idx % 25 == 0) # Raros casos para teste
    
    return {
        'first_name': first,
        'middle_name': mid,
        'last_name': last,
        'full_name': full_name,
        'cpf': cpf,
        'mother_name': mother_name,
        'city': city,
        'state_abbr': state_abbr,
        'street': street,
        'street2': street2,
        'zip': zip_code,
        'phone': phone,
        'race': race,
        'has_disability': has_disability,
    }

def log(msg):
    print(f"[MPTRCS-LOADER] {msg}")

def run_import():
    log(f"Iniciando carga completa e fidedigna no banco '{DB_NAME}'...")
    odoo.tools.config.parse_config(['-c', CONFIG_PATH, '-d', DB_NAME, '--no-http'])
    
    registry = Registry(DB_NAME)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Países e Estados
        country_br = env['res.country'].search([('code', '=', 'BR')], limit=1)
        state_sp = env['res.country.state'].search([('code', '=', 'SP'), ('country_id', '=', country_br.id)], limit=1)
        
        # 1. IES IPEN-CNEN/SP
        log("Passo 1: Configurando Empresa/IES IPEN-CNEN/SP...")
        company = env['res.company'].search([('cnpj', '=', '00.394.429/0001-00')], limit=1)
        if not company:
            company = env['res.company'].search([], limit=1)
            company.write({
                'name': 'Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP',
                'cnpj': '00.394.429/0001-00',
                'emec_code': '1902',
                'street': 'Av. Prof. Lineu Prestes, 2242 - Cidade Universitária',
                'city': 'São Paulo',
                'state_id': state_sp.id if state_sp else False,
                'country_id': country_br.id if country_br else False,
                'zip': '05508-000',
                'phone': '(11) 3133-9000',
                'email': 'posgrad@ipen.br',
            })
        log(f"Empresa configurada: ID={company.id} ({company.name})")

        # 1.1 Departamentos do OpenEduCat: op.department
        log("Passo 1.1: Configurando Departamentos OpenEduCat (op.department)...")
        dept_ctr = env['op.department'].search([('code', '=', 'CTR-IPEN')], limit=1)
        if not dept_ctr:
            dept_ctr = env['op.department'].create({
                'name': 'Centro de Tecnologia das Radiações (CTR)',
                'code': 'CTR-IPEN',
            })
        dept_cpg = env['op.department'].search([('code', '=', 'CPG-IPEN')], limit=1)
        if not dept_cpg:
            dept_cpg = env['op.department'].create({
                'name': 'Comissão de Pós-Graduação (CPG)',
                'code': 'CPG-IPEN',
            })
        dept_sec = env['op.department'].search([('code', '=', 'SECPG-IPEN')], limit=1)
        if not dept_sec:
            dept_sec = env['op.department'].create({
                'name': 'Secretaria de Pós-Graduação (SEC-PG)',
                'code': 'SECPG-IPEN',
            })
        log(f"3 Departamentos configurados: CTR-IPEN ({dept_ctr.id}), CPG-IPEN ({dept_cpg.id}), SECPG-IPEN ({dept_sec.id})")

        # 1.2 Categorias do OpenEduCat: op.category
        log("Passo 1.2: Configurando Categorias OpenEduCat (op.category)...")
        categories_data = [
            ('REG-MPTRCS', 'Aluno Regular MPTRCS'),
            ('ESP-MPTRCS', 'Aluno Especial / Avulso'),
            ('DOC-PERM', 'Docente Permanente CPG'),
            ('DOC-COLAB', 'Docente Colaborador'),
            ('REP-DISC', 'Representante Discente CPG'),
        ]
        cat_map = {}
        for c_code, c_name in categories_data:
            cat = env['op.category'].search([('code', '=', c_code)], limit=1)
            if not cat:
                cat = env['op.category'].create({
                    'name': c_name,
                    'code': c_code,
                    'company_id': company.id,
                })
            cat_map[c_code] = cat
        log(f"{len(cat_map)} Categorias configuradas no OpenEduCat!")

        # 1.3 Anos Acadêmicos e Termos (Semestres): op.academic.year / op.academic.term
        log("Passo 1.3: Configurando Anos Acadêmicos e Termos Letivos (2022 a 2026)...")
        acad_year_map = {}
        acad_term_map = {}
        for y in range(2022, 2027):
            ay = env['op.academic.year'].search([('name', '=', f"Ano Acadêmico {y}")], limit=1)
            if not ay:
                ay = env['op.academic.year'].create({
                    'name': f"Ano Acadêmico {y}",
                    'start_date': f"{y}-01-01",
                    'end_date': f"{y}-12-31",
                    'term_structure': 'two_sem',
                    'company_id': company.id,
                })
            acad_year_map[y] = ay

            for sem_idx, (s_name, dt_start, dt_end) in enumerate([
                (f"{y}.1", f"{y}-02-01", f"{y}-06-30"),
                (f"{y}.2", f"{y}-08-01", f"{y}-12-15")
            ], start=1):
                term = env['op.academic.term'].search([('name', '=', s_name), ('academic_year_id', '=', ay.id)], limit=1)
                if not term:
                    term = env['op.academic.term'].create({
                        'name': s_name,
                        'academic_year_id': ay.id,
                        'term_start_date': dt_start,
                        'term_end_date': dt_end,
                        'company_id': company.id,
                    })
                acad_term_map[s_name] = term
        log(f"5 Anos Acadêmicos (2022-2026) e 10 Termos Semestrais configurados!")

        # 1.4 Nível de Programa do OpenEduCat: op.program.level
        log("Passo 1.4: Configurando Nível do Programa (op.program.level)...")
        prog_level = env['op.program.level'].search([('name', '=', 'Pós-Graduação Stricto Sensu - Mestrado Profissional')], limit=1)
        if not prog_level:
            prog_level = env['op.program.level'].create({
                'name': 'Pós-Graduação Stricto Sensu - Mestrado Profissional'
            })
        log(f"Nível de Programa configurado: ID={prog_level.id} ({prog_level.name})")

        # 1.5 Programa do OpenEduCat: op.program
        log("Passo 1.5: Configurando Programa OpenEduCat (op.program)...")
        op_program = env['op.program'].search([('code', '=', 'MPTRCS')], limit=1)
        if not op_program:
            op_program = env['op.program'].create({
                'name': 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde',
                'code': 'MPTRCS',
                'program_level_id': prog_level.id,
                'department_id': dept_ctr.id,
                'active': True,
            })
        log(f"Programa OpenEduCat configurado: ID={op_program.id} ({op_program.name})")

        # 2. Curso Base: op.course
        log("Passo 2: Configurando Curso Base (op.course)...")
        course = env['op.course'].search([('code', '=', 'MPTRCS')], limit=1)
        if not course:
            course = env['op.course'].create({
                'name': 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde',
                'code': 'MPTRCS',
                'evaluation_type': 'normal',
                'program_id': op_program.id,
                'department_id': dept_ctr.id,
            })
        else:
            course.write({
                'program_id': op_program.id,
                'department_id': dept_ctr.id,
            })
        log(f"Curso Base configurado: ID={course.id} ({course.name})")

        # 2.1 Lotes / Turmas: op.batch
        log("Passo 2.1: Configurando Lotes / Turmas (op.batch)...")
        batch_map = {}
        for t_idx, y_start, y_end in [
            (1, 2022, 2024),
            (2, 2023, 2025),
            (3, 2024, 2026),
            (4, 2025, 2027),
        ]:
            b_code = f"MPTRCS-T{t_idx}"
            batch = env['op.batch'].search([('code', '=', b_code)], limit=1)
            if not batch:
                batch = env['op.batch'].create({
                    'name': f"Turma {t_idx} ({y_start})",
                    'code': b_code,
                    'course_id': course.id,
                    'start_date': f"{y_start}-03-01",
                    'end_date': f"{y_end}-04-30",
                    'active': True,
                })
            batch_map[t_idx] = batch
        log(f"4 Lotes/Turmas configurados no OpenEduCat (MPTRCS-T1 a MPTRCS-T4)!")

        # 3. Programa CAPES: op.program.capes
        log("Passo 3: Configurando Programa CAPES (op.program.capes)...")
        program = env['op.program.capes'].search([('snpg_code', '=', '33002010001P0')], limit=1)
        if not program:
            program = env['op.program.capes'].create({
                'name': 'Mestrado Profissional em Tecnologia das Radiações em Ciências da Saúde',
                'snpg_code': '33002010001P0',
                'modality': 'professional',
                'capes_grade': '4',
                'company_id': company.id,
                'evaluation_area': 'Medicina III / Física Médica',
                'start_date': '2021-03-01',
                'status': 'active',
                'website': 'https://www.ipen.br/pos-graduacao/mptrcs',
                'phone': '(11) 3133-9123',
            })
        log(f"Programa CAPES configurado: ID={program.id} ({program.name})")

        # 4. Áreas de Concentração e Linhas de Pesquisa (Ontologia GoPG / DAV)
        log("Passo 4: Configurando Áreas de Concentração e Linhas de Pesquisa...")
        # Área 1: Radioterapia e Dosimetria
        area_dos = env['op.program.concentration.area'].search([('code', '=', 'RAD-DOS'), ('program_id', '=', program.id)], limit=1)
        if not area_dos:
            area_dos = env['op.program.concentration.area'].create({
                'name': 'Radioterapia e Dosimetria das Radiações',
                'code': 'RAD-DOS',
                'program_id': program.id,
                'description': 'Pesquisa aplicada ao controle dosimétrico, aceleradores clínicos e segurança radiológica em oncologia.',
            })
        
        line_dos_1 = env['op.program.research.line'].search([('code', '=', 'RAD-DOS-01'), ('area_id', '=', area_dos.id)], limit=1)
        if not line_dos_1:
            line_dos_1 = env['op.program.research.line'].create({
                'name': 'Dosimetria Clínica e Planejamento Radioterápico Avançado',
                'code': 'RAD-DOS-01',
                'area_id': area_dos.id,
                'description': 'Desenvolvimento de protocolos dosimétricos clínicos, calibração de feixes e simulação Monte Carlo.',
            })

        line_dos_2 = env['op.program.research.line'].search([('code', '=', 'RAD-DOS-02'), ('area_id', '=', area_dos.id)], limit=1)
        if not line_dos_2:
            line_dos_2 = env['op.program.research.line'].create({
                'name': 'Controle da Qualidade e Segurança em Feixes de Radiação Ionizante',
                'code': 'RAD-DOS-02',
                'area_id': area_dos.id,
                'description': 'Desenvolvimento de dispositivos, fantomas e softwares para controle de garantia da qualidade em radioterapia.',
            })

        # Área 2: Medicina Nuclear e Radiofarmácia
        area_nuc = env['op.program.concentration.area'].search([('code', '=', 'RAD-NUC'), ('program_id', '=', program.id)], limit=1)
        if not area_nuc:
            area_nuc = env['op.program.concentration.area'].create({
                'name': 'Medicina Nuclear e Radiofarmácia',
                'code': 'RAD-NUC',
                'program_id': program.id,
                'description': 'Investigação e desenvolvimento de moléculas marcadas, radiofármacos inovadores e quantificação por imagem molecular.',
            })

        line_nuc_1 = env['op.program.research.line'].search([('code', '=', 'RAD-NUC-01'), ('area_id', '=', area_nuc.id)], limit=1)
        if not line_nuc_1:
            line_nuc_1 = env['op.program.research.line'].create({
                'name': 'Desenvolvimento e Caracterização de Radiofármacos Diagnósticos e Terapêuticos',
                'code': 'RAD-NUC-01',
                'area_id': area_nuc.id,
                'description': 'Síntese, purificação, controle de qualidade biológico e ensaios pré-clínicos de novos radiofármacos.',
            })

        line_nuc_2 = env['op.program.research.line'].search([('code', '=', 'RAD-NUC-02'), ('area_id', '=', area_nuc.id)], limit=1)
        if not line_nuc_2:
            line_nuc_2 = env['op.program.research.line'].create({
                'name': 'Instrumentação Nuclear, Dosimetria Interna e Imagens Moleculares',
                'code': 'RAD-NUC-02',
                'area_id': area_nuc.id,
                'description': 'Algoritmos de reconstrução tomográfica PET/SPECT, dosimetria personalizada e processamento de imagens biomédicas.',
            })

        all_lines = [line_dos_1, line_dos_2, line_nuc_1, line_nuc_2]
        log(f"Áreas e Linhas criadas: 2 Áreas ({area_dos.code}, {area_nuc.code}) e 4 Linhas de Pesquisa cadastradas!")

        # 5. Versão Curricular / Regimento (MP-TRCS v2)
        log("Passo 5: Configurando Regimento Curricular (op.curriculum.version)...")
        reg = env['op.curriculum.version'].search([('name', 'like', 'Regulamento MP-TRCS v2%'), ('program_id', '=', program.id)], limit=1)
        if not reg:
            reg = env['op.curriculum.version'].create({
                'name': 'Regulamento MP-TRCS v2 (2024)',
                'program_id': program.id,
                'min_credits': 100,
                'min_subject_credits': 40,
                'thesis_credits': 52,
                'other_mandatory_credits': 8,
                'credit_hour_ratio': 15.0,
                'max_external_credits_percent': 50.0,
                'max_months_defense': 24,
                'allow_special_students': False,
                'max_special_subjects_limit': 0,
                'special_credit_validity_months': 36,
                'special_incorporation_workflow': 'cpg_approval',
                'special_transcript_fail_policy': 'omit_on_regular',
                'allow_intra_ies_credits': False,
                'max_intra_ies_credits_percent': 0.0,
                'intra_ies_advisor_approval_required': True,
                'retorno_rule': 'current_matrix',
                'grading_scale_type': 'scale_abc_r',
                'proficiency_stage': 'admission',
                'teaching_internship_mode': 'not_applicable',
                'ptt_validation_mode': 'cpg_checklist',
                'defense_location_policy': 'hybrid_allowed',
            })
        log(f"Regimento configurado: ID={reg.id} ({reg.name})")

        # 6. Docentes e Credenciamentos CPG: op.faculty
        log("Passo 6: Cadastrando 12 Docentes com Censo Completo e Vínculos Temáticos...")
        faculty_list = []
        doc_specialties = [
            ("Física Médica e Radioterapia", area_dos, [line_dos_1, line_dos_2]),
            ("Dosimetria das Radiações", area_dos, [line_dos_1]),
            ("Proteção Radiológica em Saúde", area_dos, [line_dos_2]),
            ("Instrumentação Nuclear", area_nuc, [line_nuc_2]),
            ("Radiofarmácia e Radioimunologia", area_nuc, [line_nuc_1]),
            ("Medicina Nuclear Clínica", area_nuc, [line_nuc_1, line_nuc_2]),
            ("Controle de Qualidade em Radioterapia", area_dos, [line_dos_2]),
            ("Biofísica e Imagem Molecular", area_nuc, [line_nuc_2]),
            ("Química de Radioisótopos", area_nuc, [line_nuc_1]),
            ("Planejamento Computacional 3D/IMRT", area_dos, [line_dos_1]),
            ("Engenharia Biomédica", area_dos, [line_dos_1, line_dos_2]),
            ("Radiobiologia Celular", area_nuc, [line_nuc_1]),
        ]

        for idx in range(1, 13):
            g_letter = 'm' if idx % 2 != 0 else 'f'
            ident = gen_unique_identity(idx + 10, g_letter, is_faculty=True)
            doc_title = "Prof. Dr." if g_letter == 'm' else "Profa. Dra."
            honorific_name = f"{doc_title} {ident['full_name']}"
            email = f"{ident['first_name'].lower()}.{ident['last_name'].lower()}@ipen.br"
            b_year = 1965 + (idx % 18)
            spec_title, doc_area, doc_lines = doc_specialties[idx - 1]
            
            st_sp = env['res.country.state'].search([('code', '=', ident['state_abbr']), ('country_id', '=', country_br.id)], limit=1) or state_sp
            
            fac = env['op.faculty'].search([('cpf', '=', ident['cpf'])], limit=1)
            if not fac:
                partner = env['res.partner'].create({
                    'name': honorific_name,
                    'email': email,
                    'phone': ident['phone'],
                    'street': ident['street'],
                    'street2': ident['street2'],
                    'city': ident['city'],
                    'state_id': st_sp.id if st_sp else False,
                    'zip': ident['zip'],
                    'country_id': country_br.id if country_br else False,
                    'is_company': False,
                })
                fac = env['op.faculty'].create({
                    'partner_id': partner.id,
                    'first_name': ident['first_name'],
                    'middle_name': ident['middle_name'],
                    'last_name': ident['last_name'],
                    'gender': 'female' if (ident.get('gender_letter') == 'f' or g_letter == 'f') else 'male',
                    'birth_date': f"{b_year}-04-12",
                    'cpf': ident['cpf'],
                    'email': email,
                    'phone': ident['phone'],
                    'orcid': f"0000-0001-9000-{idx:04d}",
                    'lattes_url': f"http://lattes.cnpq.br/{ident['cpf']}0001",
                    'mother_name': ident['mother_name'],
                    'race_color': ident['race'],
                    'has_disability': ident['has_disability'],
                    'birth_city_name': ident['city'],
                    'birth_state': ident['state_abbr'],
                    'birth_country_id': country_br.id if country_br else False,
                    'nationality': country_br.id if country_br else False,
                    'work_regime': 'exclusive' if idx % 3 != 0 else 'fulltime',
                    'workload': 40,
                    'degree_level': 'phd',
                    'degree_area': spec_title,
                    'degree_ies': 'Universidade de São Paulo - USP',
                    'concentration_area_ids': [(6, 0, [doc_area.id])],
                    'research_line_ids': [(6, 0, [l.id for l in doc_lines])],
                })
            
            # Credenciamento CPG no programa
            link = env['op.faculty.program.link'].search([('faculty_id', '=', fac.id), ('program_id', '=', program.id)], limit=1)
            if not link:
                link = env['op.faculty.program.link'].create({
                    'faculty_id': fac.id,
                    'program_id': program.id,
                })
                env['op.faculty.category.ledger'].create({
                    'program_link_id': link.id,
                    'category': 'permanent',
                    'start_date': '2021-01-01',
                    'document_ref': f"Portaria CPG-IPEN {idx:03d}/2021",
                    'notes': f"Credenciamento Permanente - Área {doc_area.name}",
                })
            faculty_list.append(fac)

        log(f"12 Docentes cadastrados com identificadores biométricos e censitários completos!")

        # 6.1 Perfis de Usuários do Sistema: res.users
        log("Passo 6.1: Configurando Perfis de Usuários do Sistema (res.users)...")
        g_user = env.ref('base.group_user')
        g_admin = env.ref('openeducat_core.group_op_back_office_admin')
        g_fac = env.ref('openeducat_core.group_op_faculty')

        # Usuário Secretaria
        user_sec = env['res.users'].search([('login', '=', 'secretaria')], limit=1)
        if not user_sec:
            user_sec = env['res.users'].create({
                'name': 'Secretaria de Pós-Graduação (MPTRCS)',
                'login': 'secretaria',
                'email': 'secretaria.mptrcs@ipen.br',
                'password': 'secretaria123',
                'group_ids': [(6, 0, [g_user.id, g_admin.id])],
            })
        else:
            user_sec.write({
                'group_ids': [(4, g_admin.id)],
                'password': 'secretaria123',
            })

        # Usuário Coordenação (associado ao Prof. André Soares Muniz)
        user_coord = env['res.users'].search([('login', '=', 'coordenador')], limit=1)
        if not user_coord:
            user_coord = env['res.users'].create({
                'name': 'Prof. Dr. André Soares Muniz (Coordenador MPTRCS)',
                'login': 'coordenador',
                'email': 'coordenacao.mptrcs@ipen.br',
                'password': 'coordenador123',
                'partner_id': faculty_list[0].partner_id.id,
                'group_ids': [(6, 0, [g_user.id, g_admin.id, g_fac.id])],
            })
        else:
            user_coord.write({
                'partner_id': faculty_list[0].partner_id.id,
                'password': 'coordenador123',
                'group_ids': [(4, g_admin.id), (4, g_fac.id)],
            })

        # Usuário Vice-Coordenação (associada à Profa. Ana Cardoso Pontes)
        user_vice = env['res.users'].search([('login', '=', 'vicecoordenador')], limit=1)
        if not user_vice:
            user_vice = env['res.users'].create({
                'name': 'Profa. Dra. Ana Cardoso Pontes (Vice-Coordenadora MPTRCS)',
                'login': 'vicecoordenador',
                'email': 'vicecoordenacao.mptrcs@ipen.br',
                'password': 'vicecoordenador123',
                'partner_id': faculty_list[1].partner_id.id,
                'group_ids': [(6, 0, [g_user.id, g_admin.id, g_fac.id])],
            })
        else:
            user_vice.write({
                'partner_id': faculty_list[1].partner_id.id,
                'password': 'vicecoordenador123',
                'group_ids': [(4, g_admin.id), (4, g_fac.id)],
            })

        # Usuário Professor (associado ao Prof. Bruno Fernandes Sardenberg)
        user_prof = env['res.users'].search([('login', '=', 'professor')], limit=1)
        if not user_prof:
            user_prof = env['res.users'].create({
                'name': 'Prof. Dr. Bruno Fernandes Sardenberg',
                'login': 'professor',
                'email': 'bruno.sardenberg@ipen.br',
                'password': 'professor123',
                'partner_id': faculty_list[2].partner_id.id,
                'group_ids': [(6, 0, [g_user.id, g_fac.id])],
            })
        else:
            user_prof.write({
                'partner_id': faculty_list[2].partner_id.id,
                'password': 'professor123',
                'group_ids': [(4, g_fac.id)],
            })
        log("4 Perfis de Usuários configurados: secretaria, coordenador, vicecoordenador e professor!")

        # 7. Projetos de Pesquisa Institucionais com Fomento: capes.research.project
        log("Passo 7: Configurando Projetos de Pesquisa e Fomento...")
        projects = []
        proj_data = [
            ("Desenvolvimento de Fantomas e Sensores para Dosimetria 3D em Radioterapia", faculty_list[0], line_dos_1, "FAPESP", "2021/14589-2", "applied"),
            ("Controle de Qualidade Automatizado em Aceleradores Médicos Lineares", faculty_list[1], line_dos_2, "CNPq", "408120/2021-8", "applied"),
            ("Síntese e Avaliação Biológica de Radiofármacos Marcados com Lutécio-177", faculty_list[4], line_nuc_1, "CNEN", "01300.0012/2022", "applied"),
            ("Quantificação e Reconstrução de Imagens Moleculares em PET/CT", faculty_list[5], line_nuc_2, "IAEA", "BRA/6/029", "applied"),
        ]
        for p_title, coord, rline, agency, proc_no, nature in proj_data:
            proj = env['capes.research.project'].search([('name', '=', p_title)], limit=1)
            if not proj:
                proj = env['capes.research.project'].create({
                    'name': p_title,
                    'program_id': program.id,
                    'coordinator_id': coord.id,
                    'research_line_id': rline.id,
                    'research_nature': nature,
                    'funding_agency': agency,
                    'funding_process': proc_no,
                    'start_date': '2021-03-01',
                    'end_date': '2026-12-31',
                    'status': 'ongoing',
                    'description': f"Projeto aprovado no âmbito do MPTRCS sob fomento da agência {agency}.",
                })
            projects.append(proj)
        log(f"4 Projetos de pesquisa associados às Linhas de Pesquisa e coordenados pelos docentes!")

        # 8. Disciplinas do Catálogo: op.subject
        log("Passo 8: Cadastrando Disciplinas do Catálogo...")
        subjects_data = [
            ('RAD501', 'Fundamentos de Radiobiologia e Proteção Radiológica', 'compulsory', area_dos.name, 4, 60, [faculty_list[0], faculty_list[2]]),
            ('RAD502', 'Metodologia Científica e Elaboração de PTT', 'compulsory', area_dos.name, 4, 60, [faculty_list[1], faculty_list[6]]),
            ('RAD503', 'Seminários Gerais em Tecnologia das Radiações', 'compulsory', area_nuc.name, 2, 30, [faculty_list[3], faculty_list[5]]),
            ('RAD510', 'Dosimetria Física e Clínica em Radioterapia', 'elective', area_dos.name, 4, 60, [faculty_list[0], faculty_list[9]]),
            ('RAD511', 'Controle de Qualidade em Aceleradores Lineares', 'elective', area_dos.name, 4, 60, [faculty_list[1], faculty_list[6]]),
            ('RAD512', 'Braquiterapia Avançada e Implante de Sementes', 'elective', area_dos.name, 4, 60, [faculty_list[9], faculty_list[10]]),
            ('RAD520', 'Radiofarmácia e Radioimunologia', 'elective', area_nuc.name, 4, 60, [faculty_list[4], faculty_list[8]]),
            ('RAD521', 'Instrumentação em PET/SPECT e Imagem Molecular', 'elective', area_nuc.name, 4, 60, [faculty_list[3], faculty_list[7]]),
            ('RAD522', 'Gerenciamento de Rejeitos Radioativos em Serviços de Saúde', 'elective', area_nuc.name, 4, 60, [faculty_list[2], faculty_list[11]]),
        ]
        subject_map = {}
        for code, sname, stype, area_name, creds, hrs, fac_instructors in subjects_data:
            sub = env['op.subject'].search([('code', '=', code)], limit=1)
            if not sub:
                sub = env['op.subject'].create({
                    'name': sname,
                    'code': code,
                    'type': 'theory',
                    'subject_type': stype,
                    'program_id': program.id,
                    'grade_weightage': creds,
                    'allow_special_students': False,
                    'special_seats_quota': 0,
                    'special_student_instructor_consent_required': True,
                })
            # Vincula docentes ministrantes à disciplina
            for f_inst in fac_instructors:
                if sub.id not in f_inst.faculty_subject_ids.ids:
                    f_inst.write({'faculty_subject_ids': [(4, sub.id)]})
                    
            subject_map[code] = sub

            rule = env['op.curriculum.subject.rule'].search([('curriculum_version_id', '=', reg.id), ('subject_id', '=', sub.id)], limit=1)
            if not rule:
                env['op.curriculum.subject.rule'].create({
                    'curriculum_version_id': reg.id,
                    'subject_id': sub.id,
                    'area_name': area_name,
                    'scope': 'program' if stype == 'compulsory' else 'area',
                })
        # Atualiza o Curso Base com as 9 disciplinas do Catálogo e o Departamento
        course.write({
            'subject_ids': [(6, 0, [s.id for s in subject_map.values()])],
            'department_id': dept_ctr.id,
        })
        for sub in subject_map.values():
            sub.write({'department_id': dept_ctr.id})
        log(f"9 Disciplinas atreladas ao Curso Base MPTRCS, ao Departamento CTR e ao regimento!")

        # 9. Editais de Admissão
        log("Passo 9: Configurando Editais de Admissão (Turmas 1 a 4)...")
        edital_map = {}
        for t_num in range(1, 5):
            year = 2021 + t_num
            ed_code = f"EDITAL-MPTRCS-{year}"
            ed = env['op.admission.edital'].search([('code', '=', ed_code)], limit=1)
            if not ed:
                ed = env['op.admission.edital'].create({
                    'name': f"Edital Processo Seletivo MPTRCS - Turma {t_num} ({year})",
                    'code': ed_code,
                    'program_id': program.id,
                    'curriculum_version_id': reg.id,
                    'academic_year': str(year),
                    'total_slots': 15,
                    'start_date': f'{year-1}-10-01',
                    'end_date': f'{year-1}-12-15',
                    'affirmative_action_percent': 20.0,
                    'state': 'homologated' if t_num <= 3 else 'published',
                })
            edital_map[t_num] = ed

        # 10. Discentes, Vínculos, Planos de Trabalho, Livros-Razão, Ritos, PTTs e Diplomas
        log("Passo 10: Ingerindo 60 Discentes com Nomes 100% Únicos e Dados Censitários Completos...")
        
        ptt_axis_tech = env['capes.ptt.axis'].search([('name', 'like', 'Produtos e Processos Tecnológicos%')], limit=1) or env['capes.ptt.axis'].search([], limit=1)
        ptt_type_software = env['capes.ptt.type'].search([('code', '=', 'T19')], limit=1)
        ptt_type_protocol = env['capes.ptt.type'].search([('code', '=', 'T07')], limit=1)
        ptt_type_manual = env['capes.ptt.type'].search([('code', '=', 'T09')], limit=1)
        ptt_type_patent = env['capes.ptt.type'].search([('code', '=', 'T13')], limit=1)
        dummy_pdf = base64.b64encode(b"%PDF-1.4 Mock Plano de Trabalho MPTRCS").decode('utf-8')

        total_students = 0
        total_ledger_entries = 0
        total_theses = 0
        total_ptts = 0
        total_diplomas = 0

        t_profiles = {
            1: {'year': 2022, 'n_tit': 15, 'n_cur': 0},
            2: {'year': 2023, 'n_tit': 15, 'n_cur': 0},
            3: {'year': 2024, 'n_tit': 12, 'n_cur': 3},
            4: {'year': 2025, 'n_tit': 0, 'n_cur': 15},
        }

        global_student_counter = 0
        all_student_records = []

        for t_num, prof in t_profiles.items():
            year = prof['year']
            n_tit = prof['n_tit']
            log(f"  Processando Turma {t_num} ({year}) - {n_tit} Titulados / {prof['n_cur']} Em Curso...")

            for s_idx in range(1, 16):
                global_student_counter += 1
                total_students += 1
                
                g_letter = 'f' if (global_student_counter % 2 == 0) else 'm'
                ident = gen_unique_identity(global_student_counter + 100, g_letter)
                
                ra = f"RA{year}{s_idx:03d}"
                email = f"{ident['first_name'].lower()}.{ident['last_name'].lower()}@ipen.br"
                b_year = 1992 + (global_student_counter % 8)
                
                is_alumni = (s_idx <= n_tit)
                stu_cat = 'alumni' if is_alumni else 'regular'
                capes_stat = 'graduated' if is_alumni else 'enrolled'
                
                # Orientador e Coorientador
                advisor = faculty_list[(global_student_counter - 1) % len(faculty_list)]
                coadvisor = faculty_list[(global_student_counter + 3) % len(faculty_list)] if (global_student_counter % 4 == 0) else False
                
                # Linha de Pesquisa do Aluno
                student_line = all_lines[(global_student_counter - 1) % len(all_lines)]
                
                st_sp = env['res.country.state'].search([('code', '=', ident['state_abbr']), ('country_id', '=', country_br.id)], limit=1) or state_sp
                
                stu = env['op.student'].search([('gr_no', '=', ra)], limit=1)
                if not stu:
                    partner = env['res.partner'].create({
                        'name': ident['full_name'],
                        'email': email,
                        'phone': ident['phone'],
                        'street': ident['street'],
                        'street2': ident['street2'],
                        'city': ident['city'],
                        'state_id': st_sp.id if st_sp else False,
                        'zip': ident['zip'],
                        'country_id': country_br.id if country_br else False,
                        'is_company': False,
                    })
                    stu = env['op.student'].create({
                        'partner_id': partner.id,
                        'first_name': ident['first_name'],
                        'middle_name': ident['middle_name'],
                        'last_name': ident['last_name'],
                        'gender': 'f' if g_letter == 'f' else 'm',
                        'birth_date': f"{b_year}-07-22",
                        'gr_no': ra,
                        'ra_number': ra,
                        'cpf': ident['cpf'],
                        'email': email,
                        'phone': ident['phone'],
                        'orcid': f"0000-0002-{global_student_counter + 3000:04d}-{(global_student_counter * 7) % 9000:04d}",
                        'lattes_url': f"http://lattes.cnpq.br/{ident['cpf']}0002",
                        'mother_name': ident['mother_name'],
                        'race_color': ident['race'],
                        'has_disability': ident['has_disability'],
                        'birth_city_name': ident['city'],
                        'birth_state': ident['state_abbr'],
                        'birth_country_id': country_br.id if country_br else False,
                        'nationality': country_br.id if country_br else False,
                        'highest_degree': 'bachelor',
                        'academic_level': 'grad',
                        'company_id': company.id,
                        'student_category': stu_cat,
                        'capes_status': capes_stat,
                        'admission_date': f"{year}-03-01",
                        'advisor_id': advisor.id,
                        'coadvisor_id': coadvisor.id if coadvisor else False,
                        'english_proficiency_status': 'approved',
                        'portuguese_proficiency_status': 'not_applicable',
                    })

                all_student_records.append(stu)

                # Vínculo com o Curso: op.student.course
                sc = env['op.student.course'].search([('student_id', '=', stu.id), ('course_id', '=', course.id)], limit=1)
                if not sc:
                    sc = env['op.student.course'].create({
                        'student_id': stu.id,
                        'course_id': course.id,
                        'batch_id': batch_map[t_num].id,
                        'program_id': program.id,
                        'curriculum_version_id': reg.id,
                        'course_type': 'regular',
                        'state': 'finished' if is_alumni else 'running',
                        'admission_date': f"{year}-03-01",
                        'completion_date': f"{year+2}-04-15" if is_alumni else False,
                    })
                else:
                    sc.write({'batch_id': batch_map[t_num].id})

                # Plano de Trabalho: op.student.work_plan
                wp = env['op.student.work_plan'].search([('student_id', '=', stu.id)], limit=1)
                if not wp:
                    wp = env['op.student.work_plan'].create({
                        'name': f"Plano de Investigação e Desenvolvimento Tecnológico: {ident['full_name']}",
                        'student_id': stu.id,
                        'advisor_id': advisor.id,
                        'research_line_id': student_line.id,
                        'research_line': student_line.name,
                        'summary': f"Desenvolvimento de tecnologia radiológica no âmbito da Linha '{student_line.name}'. Investigação conduzida pelo discente {ident['full_name']}.",
                        'methodology': "Ensaios laboratoriais e dosimétricos com feixes clínicos, dosimetria termoluminescente e modelagem computacional.",
                        'opinion_category': 'approved',
                        'cep_approved': True,
                        'attachment_pdf': dummy_pdf,
                        'state': 'homologated',
                    })

                # Livro-Razão Acadêmico: op.student.credit.ledger
                existing_ledger = env['op.student.credit.ledger'].search_count([('student_id', '=', stu.id)])
                if existing_ledger == 0:
                    # 3 Disciplinas Obrigatórias (10 créditos)
                    for code in ['RAD501', 'RAD502', 'RAD503']:
                        sub = subject_map[code]
                        env['op.student.credit.ledger'].create({
                            'student_id': stu.id,
                            'curriculum_version_id': reg.id,
                            'subject_id': sub.id,
                            'course_name': sub.name,
                            'credit_type': 'subject_internal',
                            'credits': sub.grade_weightage,
                            'grade_concept': 'A' if s_idx % 2 == 0 else 'B',
                            'is_approved': True,
                            'date_earned': f"{year}-06-30",
                            'origin_ref': f"MPTRCS Turma {t_num} Semestre 1",
                        })
                        total_ledger_entries += 1

                    # 6 Disciplinas Eletivas (24 créditos)
                    if is_alumni or t_num == 3:
                        for code in ['RAD510', 'RAD511', 'RAD512', 'RAD520', 'RAD521', 'RAD522']:
                            sub = subject_map[code]
                            env['op.student.credit.ledger'].create({
                                'student_id': stu.id,
                                'curriculum_version_id': reg.id,
                                'subject_id': sub.id,
                                'course_name': sub.name,
                                'credit_type': 'subject_internal',
                                'credits': sub.grade_weightage,
                                'grade_concept': 'A' if s_idx % 3 != 0 else 'B',
                                'is_approved': True,
                                'date_earned': f"{year}-12-15",
                                'origin_ref': f"MPTRCS Turma {t_num} Semestre 2",
                            })
                            total_ledger_entries += 1

                    if is_alumni:
                        # Atividades Complementares / PTT (8 créditos)
                        env['op.student.credit.ledger'].create({
                            'student_id': stu.id,
                            'curriculum_version_id': reg.id,
                            'course_name': 'Seminários de Acompanhamento e Desenvolvimento de PTT',
                            'credit_type': 'apo',
                            'credits': 8,
                            'grade_concept': 'A',
                            'is_approved': True,
                            'date_earned': f"{year+1}-11-30",
                            'origin_ref': f"MPTRCS Turma {t_num} APO",
                        })
                        total_ledger_entries += 1

                        # Defesa de Dissertação e Produto Tecnológico (52 créditos)
                        env['op.student.credit.ledger'].create({
                            'student_id': stu.id,
                            'curriculum_version_id': reg.id,
                            'course_name': 'Defesa Pública de Dissertação e Produto Tecnológico',
                            'credit_type': 'milestone',
                            'credits': 52,
                            'grade_concept': 'A',
                            'is_approved': True,
                            'date_earned': f"{year+2}-04-15",
                            'origin_ref': f"Banca Defesa Turma {t_num}",
                        })
                        total_ledger_entries += 1

                # Ritos, Defesas, Bancas, PTT e Diploma para Egressos/Titulados
                if is_alumni:
                    defense_dt = f"{year+2}-04-15"
                    th_title = f"Inovação Tecnológica e Avaliação Dosimétrica em Aplicações Médicas Nucleares - Estudo de Caso {ident['last_name']}"
                    
                    thesis = env['capes.thesis'].search([('student_id', '=', stu.id)], limit=1)
                    if not thesis:
                        thesis = env['capes.thesis'].create({
                            'student_id': stu.id,
                            'work_plan_id': wp.id,
                            'title': th_title,
                            'doc_type': 'dissertation',
                            'stage': 'defense',
                            'status': 'homologated',
                            'defense_date': defense_dt,
                            'secretariat_approval': True,
                            'secretariat_approval_date': f"{year+2}-05-02",
                            'repository_url': f"http://repositorio.ipen.br/handle/123456789/{ra.lower()}",
                        })
                        total_theses += 1

                        # Membros da Banca Julgadora (Comissão Examinadora)
                        # 1. Orientador (Presidente)
                        env['capes.thesis.committee'].create({
                            'thesis_id': thesis.id,
                            'member_id': advisor.partner_id.id,
                            'member_role': 'advisor',
                            'is_titular': True,
                        })
                        # 2. Avaliador Interno
                        eval_int = faculty_list[(global_student_counter + 1) % len(faculty_list)]
                        env['capes.thesis.committee'].create({
                            'thesis_id': thesis.id,
                            'member_id': eval_int.partner_id.id,
                            'member_role': 'internal_evaluator',
                            'is_titular': True,
                        })
                        # 3. Avaliador Externo (USP / InCor / HC-FMUSP)
                        eval_ext = faculty_list[(global_student_counter + 2) % len(faculty_list)]
                        env['capes.thesis.committee'].create({
                            'thesis_id': thesis.id,
                            'member_id': eval_ext.partner_id.id,
                            'member_role': 'external_evaluator',
                            'is_titular': True,
                        })

                    # PTT Homologado
                    ptt_types = [ptt_type_software, ptt_type_protocol, ptt_type_manual, ptt_type_patent]
                    chosen_type = ptt_types[(s_idx + t_num) % len(ptt_types)] or ptt_type_software
                    ptt = env['capes.ptt.product'].search([('thesis_id', '=', thesis.id)], limit=1)
                    if not ptt:
                        ptt = env['capes.ptt.product'].create({
                            'title': f"Inovação Tecnológica Aplicada MPTRCS: {chosen_type.name} ({ident['last_name']})",
                            'type_id': chosen_type.id,
                            'axis_id': chosen_type.axis_id.id if chosen_type.axis_id else ptt_axis_tech.id,
                            'student_id': stu.id,
                            'thesis_id': thesis.id,
                            'trl_level': f'trl_{min(9, 6 + (s_idx % 4))}',
                            'adherence_justif': f"Produto estritamente aderente à Linha de Pesquisa '{student_line.name}'.",
                            'final_stratum': 'T1' if s_idx % 3 == 0 else ('T2' if s_idx % 2 == 0 else 'T3'),
                            'repository_url': f"http://repositorio.ipen.br/handle/123456789/ptt-{ra.lower()}",
                            'state': 'homologated',
                        })
                        # Coautores: Aluno (main_dev) + Orientador (advisor)
                        env['capes.ptt.author'].create({
                            'product_id': ptt.id,
                            'partner_id': stu.partner_id.id,
                            'author_role': 'main_dev',
                            'ip_share': 60.0,
                        })
                        env['capes.ptt.author'].create({
                            'product_id': ptt.id,
                            'partner_id': advisor.partner_id.id,
                            'author_role': 'advisor',
                            'ip_share': 40.0,
                        })
                        total_ptts += 1

                    # Diploma Digital com Registro na USP
                    diploma = env['capes.digital.diploma'].search([('thesis_id', '=', thesis.id)], limit=1)
                    if not diploma:
                        diploma = env['capes.digital.diploma'].create({
                            'student_id': stu.id,
                            'thesis_id': thesis.id,
                            'curriculum_version_id': reg.id,
                            'degree_type': 'master',
                            'issuing_ies_type': 'external_registering_university',
                            'emission_format': 'digital',
                            'origin_ies_name': 'Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP',
                            'issuing_ies_name': 'Universidade de São Paulo - USP',
                            'diploma_process_number': f"USP-PRPG-{year+2}-{global_student_counter:04d}",
                            'registration_book_number': f"LV-{year+2}",
                            'registration_page_number': f"{s_idx:03d}",
                            'graduation_date': f"{year+2}-04-15",
                            'registration_date': f"{year+2}-06-20",
                            'state': 'signed',
                        })
                        total_diplomas += 1

        # 11. Governança da CPG: Comitê, Membros, Reuniões e Atas Mensais (2022 a 2026)
        log("Passo 11: Configurando Composição da CPG, Membros Titulares/Suplentes e Atas Mensais...")
        
        # Gestão 2022-2025 (Histórica / Encerrada)
        cpg_2022 = env['op.cpg.committee'].search([('name', '=', 'Gestão CPG MPTRCS (2022-2025)')], limit=1)
        if not cpg_2022:
            cpg_2022 = env['op.cpg.committee'].create({
                'name': 'Gestão CPG MPTRCS (2022-2025)',
                'program_id': program.id,
                'start_date': '2022-01-01',
                'end_date': '2024-12-31',
                'status': 'closed',
            })

        # Gestão 2025-2028 (Ativa)
        cpg_2025 = env['op.cpg.committee'].search([('name', '=', 'Gestão CPG MPTRCS (2025-2028)')], limit=1)
        if not cpg_2025:
            cpg_2025 = env['op.cpg.committee'].create({
                'name': 'Gestão CPG MPTRCS (2025-2028)',
                'program_id': program.id,
                'start_date': '2025-01-01',
                'end_date': '2027-12-31',
                'status': 'active',
            })

        # Composição dos Membros (6 Titulares + 4 Suplentes)
        stu_rep_titular = all_student_records[0].partner_id if len(all_student_records) > 0 else faculty_list[0].partner_id
        stu_rep_suplente = all_student_records[1].partner_id if len(all_student_records) > 1 else faculty_list[1].partner_id

        committee_members_spec = [
            (faculty_list[0].partner_id, 'coordinator', 'peer_election', 'Portaria DIR-IPEN 001/2022'),
            (faculty_list[1].partner_id, 'vice_coordinator', 'peer_election', 'Portaria DIR-IPEN 002/2022'),
            (faculty_list[2].partner_id, 'titular', 'peer_election', 'Portaria DIR-IPEN 003/2022'),
            (faculty_list[3].partner_id, 'titular', 'peer_election', 'Portaria DIR-IPEN 004/2022'),
            (faculty_list[4].partner_id, 'titular', 'peer_election', 'Portaria DIR-IPEN 005/2022'),
            (stu_rep_titular, 'student_rep', 'student_election', 'Ata Eleição Representação Discente 01/2022'),
            (faculty_list[5].partner_id, 'suplente', 'peer_election', 'Portaria DIR-IPEN 006/2022'),
            (faculty_list[6].partner_id, 'suplente', 'peer_election', 'Portaria DIR-IPEN 007/2022'),
            (faculty_list[7].partner_id, 'suplente', 'peer_election', 'Portaria DIR-IPEN 008/2022'),
            (stu_rep_suplente, 'suplente', 'student_election', 'Ata Eleição Representação Discente 02/2022'),
        ]

        for comm in [cpg_2022, cpg_2025]:
            for partner, role, origin, dref in committee_members_spec:
                m_rec = env['op.cpg.member'].search([('committee_id', '=', comm.id), ('partner_id', '=', partner.id)], limit=1)
                if not m_rec:
                    env['op.cpg.member'].create({
                        'committee_id': comm.id,
                        'partner_id': partner.id,
                        'role': role,
                        'mandate_origin': origin,
                        'document_ref': dref,
                    })

        log("Composição CPG estruturada com 6 Membros Titulares e 4 Suplentes!")

        # Reuniões Ordinárias Mensais (2022 a 2026)
        log("Gerando 47 Reuniões Ordinárias da CPG com registro de Atas e Deliberações...")
        total_meetings = 0
        total_requests = 0

        # Mapeamento de pautas acadêmicas
        sample_requests_data = [
            (all_student_records[0], 'prorrogacao', 'Prorrogação de 90 dias para finalização de medições dosimétricas no acelerador linear.', 90, 'Deferido prazo extraordinário conforme Art. 42 do Regimento.'),
            (all_student_records[1], 'proficiencia', 'Homologação de certificado internacional de proficiência em língua inglesa TOEFL iBT (Pontuação: 98).', 0, 'Certificado validado e proficiência deferida com louvor.'),
            (all_student_records[15], 'credit_transfer', 'Aproveitamento de 4 créditos da disciplina cursada no Programa de Tecnologia Nuclear USP.', 0, 'Deferido aproveitamento de créditos extra-IES dentro do teto regimental.'),
            (all_student_records[16], 'coadvisor_add', 'Indicação formal de coorientador externo atuante no Instituto do Câncer do Estado de SP (ICESP).', 0, 'Indicação homologada pelo mérito técnico do coorientador.'),
            (all_student_records[30], 'trancamento', 'Trancamento de matrícula por 60 dias decorrente de tratamento de saúde com laudo médico.', 60, 'Trancamento deferido nos termos regimentais sem prejuízo de prazo.'),
            (all_student_records[31], 'ptt_homologation', 'Homologação preliminar de Produto Técnico-Tecnológico: Software de Planejamento Braquiterápico.', 0, 'Produto classificado como TRL 7 e aprovado em conformidade com o Qualis Tecnológico.'),
            (all_student_records[45], 'prorrogacao', 'Prorrogação de prazo para apresentação do Seminário Geral de Área.', 30, 'Pauta aberta para deliberação na sessão ordinária corrente.'),
        ]
        req_idx = 0

        for year in [2022, 2023, 2024, 2025, 2026]:
            comm = cpg_2022 if year <= 2024 else cpg_2025
            months = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12] if year <= 2025 else [2, 3, 4, 5, 6, 8, 9]
            
            for ord_idx, month in enumerate(months, start=1):
                total_meetings += 1
                m_name = f"{ord_idx}ª Reunião Ordinária da CPG/MPTRCS ({year})"
                is_latest = (year == 2026 and month == 9)
                m_state = 'agenda_open' if is_latest else 'published'
                m_date = f"{year}-{month:02d}-15 14:00:00"

                meeting = env['op.cpg.meeting'].search([('name', '=', m_name), ('committee_id', '=', comm.id)], limit=1)
                if not meeting:
                    meeting = env['op.cpg.meeting'].create({
                        'name': m_name,
                        'committee_id': comm.id,
                        'meeting_date': m_date,
                        'meeting_type': 'ordinary',
                        'state': m_state,
                        'minutes_pdf': dummy_pdf if m_state == 'published' else False,
                    })

                # Log de aprovação eletrônica da ata para reuniões publicadas
                if m_state == 'published':
                    existing_logs = env['op.cpg.approval.log'].search_count([('meeting_id', '=', meeting.id)])
                    if existing_logs == 0:
                        env['op.cpg.approval.log'].create({
                            'meeting_id': meeting.id,
                            'user_id': user_coord.id,
                            'timestamp': f"{year}-{month:02d}-15 16:30:00",
                            'vote': 'approve',
                            'ip_address': '10.20.1.15',
                            'notes': 'Ata aprovada e chancelada digitalmente pelo Coordenador do Programa.',
                        })
                        env['op.cpg.approval.log'].create({
                            'meeting_id': meeting.id,
                            'user_id': user_vice.id,
                            'timestamp': f"{year}-{month:02d}-15 16:32:00",
                            'vote': 'approve',
                            'ip_address': '10.20.1.18',
                            'notes': 'Concordância integral da Vice-Coordenação com as deliberações.',
                        })

                # Insere Requerimentos Acadêmicos em reuniões estratégicas
                if req_idx < len(sample_requests_data) and (ord_idx % 2 == 0 or is_latest):
                    stu_req, rtype, justif, rdays, res_notes = sample_requests_data[req_idx]
                    req_name = f"REQ-CPG-{year}-{req_idx+1:03d}"
                    existing_req = env['op.academic.request'].search([('name', '=', req_name)], limit=1)
                    if not existing_req:
                        env['op.academic.request'].create({
                            'name': req_name,
                            'student_id': stu_req.id,
                            'request_type': rtype,
                            'justification': justif,
                            'requested_days': rdays,
                            'advisor_approval': 'approved',
                            'state': 'under_review' if is_latest else 'approved',
                            'cpg_meeting_id': meeting.id,
                            'resolution_notes': res_notes,
                        })
                        total_requests += 1
                    req_idx += 1

        log(f"{total_meetings} Reuniões da CPG configuradas com Atas, Logs de Aprovação e Requerimentos Pautados!")

        cr.commit()
        log("=================================================================")
        log("Carga de dados finalizada com SUCESSO ABSOLUTO (Commit efetuado)!")
        log(f"RESUMO DO CENÁRIO MPTRCS CARREGADO:")
        log(f" - Departamentos OpenEduCat: 3 (CTR-IPEN, CPG-IPEN, SECPG-IPEN)")
        log(f" - Categorias OpenEduCat: 5 (Regular, Especial, Docente, Rep. Discente)")
        log(f" - Anos e Termos Acadêmicos: 5 Anos (2022-2026) e 10 Termos Semestrais")
        log(f" - Lotes / Turmas: 4 Turmas (MPTRCS-T1 a T4) vinculadas aos 60 discentes")
        log(f" - Usuários Criados: 4 (admin, secretaria, coordenador, vicecoordenador, professor)")
        log(f" - Gestões da CPG: 2 (2022-2025 Encerrada, 2025-2028 Ativa)")
        log(f" - Membros da CPG: 10 (6 Titulares e 4 Suplentes)")
        log(f" - Reuniões e Atas Mensais CPG: {total_meetings} reuniões (46 publicadas, 1 em pauta aberta)")
        log(f" - Requerimentos Acadêmicos Pautados: {total_requests}")
        log(f" - Áreas de Concentração: 2 (RAD-DOS e RAD-NUC)")
        log(f" - Linhas de Pesquisa: 4 (completas e vinculadas a docentes e alunos)")
        log(f" - Docentes Cadastrados: {len(faculty_list)} (com censo e vínculos 360°)")
        log(f" - Projetos de Pesquisa com Fomento: {len(projects)}")
        log(f" - Discentes Cadastrados: {total_students} (Turmas 1 a 4 - NOMES 100% ÚNICOS)")
        log(f" - Vínculos no Livro-Razão de Créditos: {total_ledger_entries}")
        log(f" - Dissertações Defendidas e Bancas Homologadas: {total_theses}")
        log(f" - Produtos Técnico-Tecnológicos (PTTs) Chancelados: {total_ptts}")
        log(f" - Diplomas Digitais (Registro USP / Protocolado): {total_diplomas}")
        log("=================================================================")

if __name__ == '__main__':
    run_import()
