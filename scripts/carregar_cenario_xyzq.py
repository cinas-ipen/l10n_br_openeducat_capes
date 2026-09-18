#!/usr/bin/env python3
"""
Carregador Completo do Cenário Universidade XYZQ no Odoo 19 (Banco universidade_xyzq)
Executa via API ORM do Odoo, ingerindo os 33 arquivos CSV sintéticos com integridade referencial:
1. Instituição IES, Departamentos, Categorias, Anos e Termos Acadêmicos, Cursos e Turmas.
2. 4 Programas CAPES (3 Acadêmicos + 1 Profissional), Regulamentos/Versões Curriculares, Áreas e Linhas.
3. 25 Docentes com censo CAPES completo, vínculos institucionais e livros-razão de credenciamento.
4. 85 Discentes (Turmas T1 a T9) com identidades únicas, planos de trabalho e livro-razão de créditos.
5. Ritos de Defesa de Teses/Dissertações, Comissões Examinadoras (Bancas), Produtos PTT e Diplomas Digitais.
6. Governança CPG (Comissões, Membros e Reuniões/Atas).
7. Usuários e Perfis de Acesso (Administração, Secretaria, Coordenação e Docência).
8. Dados de Teste de Edital e Bolsas de Estudo (Módulo de Bolsas CAPES).
"""

import os
import sys
import csv
import base64
import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

DB_NAME = 'universidade_xyzq'
CONFIG_PATH = '/etc/odoo/odoo.conf'

# Localização dos CSVs (dentro do container ou no host)
CANDIDATE_PATHS = [
    '/mnt/extra-addons/import_templates/datasets_sinteticos/universidade_xyzq',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../import_templates/datasets_sinteticos/universidade_xyzq'),
    'import_templates/datasets_sinteticos/universidade_xyzq',
]

CSV_DIR = None
for p in CANDIDATE_PATHS:
    if os.path.isdir(p):
        CSV_DIR = os.path.abspath(p)
        break

if not CSV_DIR:
    raise FileNotFoundError("Diretório de datasets sintéticos de universidade_xyzq não encontrado!")

def log(msg):
    print(f"[XYZQ-LOADER] {msg}", flush=True)

def load_csv(filename):
    filepath = os.path.join(CSV_DIR, filename)
    if not os.path.isfile(filepath):
        matches = [f for f in os.listdir(CSV_DIR) if f.startswith(filename) or filename in f]
        if matches:
            filepath = os.path.join(CSV_DIR, matches[0])
        else:
            raise FileNotFoundError(f"Arquivo CSV '{filename}' não encontrado em {CSV_DIR}")
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def register_xml_id(env, module, name, model, res_id):
    Data = env['ir.model.data']
    rec = Data.search([('module', '=', module), ('name', '=', name)], limit=1)
    if not rec:
        Data.create({
            'module': module,
            'name': name,
            'model': model,
            'res_id': res_id,
            'noupdate': True,
        })
    else:
        rec.write({'res_id': res_id, 'model': model})

def run_import():
    log(f"Iniciando carga de dados sintéticos no banco '{DB_NAME}' a partir de: {CSV_DIR}")
    odoo.tools.config.parse_config(['-c', CONFIG_PATH, '-d', DB_NAME, '--no-http'])

    registry = Registry(DB_NAME)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        id_map = {}
        person_partner_map = {}

        country_br = env['res.country'].search([('code', '=', 'BR')], limit=1)
        state_sp = env['res.country.state'].search([('code', '=', 'SP'), ('country_id', '=', country_br.id)], limit=1)

        # ----------------------------------------------------------------------
        # 1. IES Instituição: res.company
        # ----------------------------------------------------------------------
        log("Passo 1: Configurando IES Instituição (res.company)...")
        rows = load_csv('01a_ies_instituicao_res_company.csv')
        for r in rows:
            company = env['res.company'].search([], limit=1)
            company.write({
                'name': r['name'],
                'cnpj': r['cnpj'],
                'emec_code': r['emec_code'],
                'street': r['street'],
                'city': r['city'],
                'zip': r['zip'],
                'country_id': country_br.id if country_br else False,
                'state_id': state_sp.id if state_sp else False,
                'phone': '(11) 3344-5500',
                'email': 'posgraduacao@xyzq.edu.br',
            })
            id_map[r['id']] = company.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'res.company', company.id)
            log(f"  IES configurada: ID={company.id} ({company.name})")

        # ----------------------------------------------------------------------
        # 2. Departamentos: op.department
        # ----------------------------------------------------------------------
        log("Passo 2: Configurando Departamentos (op.department)...")
        rows = load_csv('01b_departamentos_op_department.csv')
        for r in rows:
            dept = env['op.department'].search([('code', '=', r['code'])], limit=1)
            if not dept:
                dept = env['op.department'].create({
                    'name': r['name'],
                    'code': r['code'],
                })
            id_map[r['id']] = dept.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.department', dept.id)
        log(f"  {len(rows)} Departamentos configurados.")

        # ----------------------------------------------------------------------
        # 3. Categorias: op.category
        # ----------------------------------------------------------------------
        log("Passo 3: Configurando Categorias OpenEduCat (op.category)...")
        rows = load_csv('01c_categorias_op_category.csv')
        for r in rows:
            cat = env['op.category'].search([('code', '=', r['code'])], limit=1)
            comp_id = id_map.get(r['company_id/id'], company.id)
            if not cat:
                cat = env['op.category'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'company_id': comp_id,
                })
            id_map[r['id']] = cat.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.category', cat.id)
        log(f"  {len(rows)} Categorias configuradas.")

        # ----------------------------------------------------------------------
        # 4. Anos Acadêmicos: op.academic.year
        # ----------------------------------------------------------------------
        log("Passo 4: Configurando Anos Acadêmicos (op.academic.year)...")
        rows = load_csv('01d_anos_academicos_op_academic_year.csv')
        for r in rows:
            comp_id = id_map.get(r['company_id/id'], company.id)
            ay = env['op.academic.year'].search([('name', '=', r['name'])], limit=1)
            if not ay:
                ay = env['op.academic.year'].create({
                    'name': r['name'],
                    'start_date': r['start_date'],
                    'end_date': r['end_date'],
                    'term_structure': r['term_structure'],
                    'company_id': comp_id,
                })
            id_map[r['id']] = ay.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.academic.year', ay.id)
        log(f"  {len(rows)} Anos Acadêmicos configurados.")

        # ----------------------------------------------------------------------
        # 5. Termos Acadêmicos: op.academic.term
        # ----------------------------------------------------------------------
        log("Passo 5: Configurando Termos Semestrais (op.academic.term)...")
        rows = load_csv('01e_termos_academicos_op_academic_term.csv')
        for r in rows:
            ay_id = id_map[r['academic_year_id/id']]
            comp_id = id_map.get(r['company_id/id'], company.id)
            term = env['op.academic.term'].search([('name', '=', r['name']), ('academic_year_id', '=', ay_id)], limit=1)
            if not term:
                term = env['op.academic.term'].create({
                    'name': r['name'],
                    'academic_year_id': ay_id,
                    'term_start_date': r['term_start_date'],
                    'term_end_date': r['term_end_date'],
                    'company_id': comp_id,
                })
            id_map[r['id']] = term.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.academic.term', term.id)
        log(f"  {len(rows)} Termos Semestrais configurados.")

        # ----------------------------------------------------------------------
        # 6. Níveis de Programa: op.program.level
        # ----------------------------------------------------------------------
        log("Passo 6: Configurando Níveis de Programa (op.program.level)...")
        rows = load_csv('01f_niveis_programa_op_program_level.csv')
        for r in rows:
            pl = env['op.program.level'].search([('name', '=', r['name'])], limit=1)
            if not pl:
                pl = env['op.program.level'].create({
                    'name': r['name'],
                })
            id_map[r['id']] = pl.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.program.level', pl.id)
        log(f"  {len(rows)} Níveis de Programa configurados.")

        # ----------------------------------------------------------------------
        # 7. Programas OpenEduCat: op.program
        # ----------------------------------------------------------------------
        log("Passo 7: Configurando Programas OpenEduCat (op.program)...")
        rows = load_csv('01g_programas_openeducat_op_program.csv')
        for r in rows:
            op_prog = env['op.program'].search([('code', '=', r['code'])], limit=1)
            if not op_prog:
                op_prog = env['op.program'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'program_level_id': id_map[r['program_level_id/id']],
                    'department_id': id_map[r['department_id/id']],
                    'active': r['active'].lower() == 'true',
                })
            id_map[r['id']] = op_prog.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.program', op_prog.id)
        log(f"  {len(rows)} Programas OpenEduCat configurados.")

        # ----------------------------------------------------------------------
        # 8. Cursos OpenEduCat: op.course
        # ----------------------------------------------------------------------
        log("Passo 8: Configurando Cursos OpenEduCat (op.course)...")
        rows = load_csv('01h_cursos_openeducat_op_course.csv')
        for r in rows:
            crs = env['op.course'].search([('code', '=', r['code'])], limit=1)
            if not crs:
                crs = env['op.course'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'evaluation_type': r['evaluation_type'],
                    'program_id': id_map[r['program_id/id']],
                    'department_id': id_map[r['department_id/id']],
                })
            id_map[r['id']] = crs.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.course', crs.id)
        log(f"  {len(rows)} Cursos OpenEduCat configurados.")

        # ----------------------------------------------------------------------
        # 9. Lotes / Turmas: op.batch
        # ----------------------------------------------------------------------
        log("Passo 9: Configurando Lotes e Turmas (op.batch)...")
        rows = load_csv('01i_lotes_turmas_op_batch.csv')
        for r in rows:
            batch = env['op.batch'].search([('code', '=', r['code'])], limit=1)
            if not batch:
                batch = env['op.batch'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'course_id': id_map[r['course_id/id']],
                    'start_date': r['start_date'],
                    'end_date': r['end_date'],
                    'active': r['active'].lower() == 'true',
                })
            id_map[r['id']] = batch.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.batch', batch.id)
        log(f"  {len(rows)} Lotes/Turmas configurados.")

        # ----------------------------------------------------------------------
        # 10. Programas CAPES: op.program.capes
        # ----------------------------------------------------------------------
        log("Passo 10: Configurando Programas CAPES (op.program.capes)...")
        rows = load_csv('02_programas_capes_op_program.csv')
        for r in rows:
            prog_capes = env['op.program.capes'].search([('snpg_code', '=', r['snpg_code'])], limit=1)
            comp_id = id_map.get(r['company_id/id'], company.id)
            if not prog_capes:
                prog_capes = env['op.program.capes'].create({
                    'name': r['name'],
                    'short_name': r['short_name'],
                    'snpg_code': r['snpg_code'],
                    'modality': r['modality'],
                    'capes_grade': r['capes_grade'],
                    'school_term': r['school_term'],
                    'company_id': comp_id,
                    'evaluation_area': r['evaluation_area'],
                    'status': r['status'],
                    'start_date': '2020-03-01',
                })
            id_map[r['id']] = prog_capes.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.program.capes', prog_capes.id)
        log(f"  {len(rows)} Programas CAPES configurados.")

        # Vínculo das Turmas (op.batch) aos Programas CAPES correspondentes
        crs_to_prog_map = {
            'crs_xyzq_cc': 'prog_xyzq_cc',
            'crs_xyzq_fis': 'prog_xyzq_fis',
            'crs_xyzq_bio': 'prog_xyzq_bio',
            'crs_xyzq_mpe': 'prog_xyzq_mpe',
        }
        for r_b in load_csv('01i_lotes_turmas_op_batch.csv'):
            b_id = id_map.get(r_b['id'])
            p_xml_id = crs_to_prog_map.get(r_b['course_id/id'])
            if b_id and p_xml_id and p_xml_id in id_map:
                env['op.batch'].browse(b_id).write({'program_id': id_map[p_xml_id]})
        log("  Turmas/Lotes associados aos respectivos Programas CAPES.")

        # ----------------------------------------------------------------------
        # 11. Versões Curriculares / Regimentos: op.curriculum.version
        # ----------------------------------------------------------------------
        log("Passo 11: Configurando Regimentos Curriculares (op.curriculum.version)...")
        rows = load_csv('03_versao_curricular_op_curriculum_version.csv')
        for r in rows:
            prog_id = id_map[r['program_id/id']]
            cv = env['op.curriculum.version'].search([('name', '=', r['name']), ('program_id', '=', prog_id)], limit=1)
            if not cv:
                cv = env['op.curriculum.version'].create({
                    'name': r['name'],
                    'program_id': prog_id,
                    'min_credits': float(r['min_credits']),
                    'min_subject_credits': float(r['min_subject_credits']),
                    'thesis_credits': float(r['thesis_credits']),
                    'other_mandatory_credits': float(r['other_mandatory_credits']),
                    'credit_hour_ratio': float(r['credit_hour_ratio']),
                    'max_external_credits_percent': float(r['max_external_credits_percent']),
                    'max_months_defense': int(r['max_months_defense']),
                    'allow_special_students': r['allow_special_students'].lower() == 'true',
                    'max_special_subjects_limit': int(r['max_special_subjects_limit']),
                    'special_credit_validity_months': int(r['special_credit_validity_months']),
                    'special_incorporation_workflow': r['special_incorporation_workflow'],
                    'special_transcript_fail_policy': r['special_transcript_fail_policy'],
                    'allow_intra_ies_credits': r['allow_intra_ies_credits'].lower() == 'true',
                    'max_intra_ies_credits_percent': float(r['max_intra_ies_credits_percent']),
                    'intra_ies_advisor_approval_required': r['intra_ies_advisor_approval_required'].lower() == 'true',
                    'retorno_rule': r['retorno_rule'],
                    'grading_scale_type': r['grading_scale_type'],
                    'proficiency_stage': r['proficiency_stage'],
                    'teaching_internship_mode': r['teaching_internship_mode'],
                    'ptt_validation_mode': r['ptt_validation_mode'],
                    'defense_location_policy': r['defense_location_policy'],
                })
            id_map[r['id']] = cv.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.curriculum.version', cv.id)
        log(f"  {len(rows)} Versões Curriculares configuradas.")

        # ----------------------------------------------------------------------
        # 12. Áreas de Concentração: op.program.concentration.area
        # ----------------------------------------------------------------------
        log("Passo 12: Configurando Áreas de Concentração (op.program.concentration.area)...")
        rows = load_csv('04a_areas_concentracao_op_program_concentration_area.csv')
        for r in rows:
            prog_id = id_map[r['program_id/id']]
            area = env['op.program.concentration.area'].search([('code', '=', r['code']), ('program_id', '=', prog_id)], limit=1)
            if not area:
                area = env['op.program.concentration.area'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'program_id': prog_id,
                    'description': r['description'],
                })
            id_map[r['id']] = area.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.program.concentration.area', area.id)
        log(f"  {len(rows)} Áreas de Concentração configuradas.")

        # ----------------------------------------------------------------------
        # 13. Linhas de Pesquisa: op.program.research.line
        # ----------------------------------------------------------------------
        log("Passo 13: Configurando Linhas de Pesquisa (op.program.research.line)...")
        rows = load_csv('04b_linhas_pesquisa_op_program_research_line.csv')
        for r in rows:
            area_id = id_map[r['area_id/id']]
            line = env['op.program.research.line'].search([('code', '=', r['code']), ('area_id', '=', area_id)], limit=1)
            if not line:
                line = env['op.program.research.line'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'area_id': area_id,
                    'description': r['description'],
                })
            id_map[r['id']] = line.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.program.research.line', line.id)
        log(f"  {len(rows)} Linhas de Pesquisa configuradas.")

        # ----------------------------------------------------------------------
        # 14. Docentes e Orientadores: op.faculty & res.partner
        # ----------------------------------------------------------------------
        log("Passo 14: Cadastrando 25 Docentes com Censo CAPES e Identidade Soberana...")
        rows = load_csv('05_docentes_orientadores_op_faculty.csv')
        for r in rows:
            st = env['res.country.state'].search([('code', '=', r['birth_state']), ('country_id', '=', country_br.id)], limit=1) or state_sp
            fac = env['op.faculty'].search([('cpf', '=', r['cpf'])], limit=1)
            if not fac:
                partner = env['res.partner'].create({
                    'name': r['name'],
                    'email': r['email'],
                    'phone': r['phone'],
                    'street': r['street'],
                    'city': r['city'],
                    'zip': r['zip'],
                    'country_id': country_br.id if country_br else False,
                    'state_id': st.id if st else False,
                    'cpf': r['cpf'],
                    'mother_name': r['mother_name'],
                    'race_color': r['race_color'],
                    'has_disability': r['has_disability'].lower() == 'true',
                    'birth_city_name': r['birth_city_name'],
                    'birth_state': r['birth_state'],
                    'orcid': r['orcid'],
                    'lattes_url': r['lattes_url'],
                    'is_company': False,
                })
                fac = env['op.faculty'].create({
                    'partner_id': partner.id,
                    'first_name': r['first_name'],
                    'middle_name': r['middle_name'],
                    'last_name': r['last_name'],
                    'gender': r['gender'],
                    'birth_date': r['birth_date'],
                    'workload': int(r['workload']) if r['workload'] else 40,
                    'work_regime': r['work_regime'],
                    'degree_level': r['degree_level'],
                    'degree_area': r['degree_area'],
                    'degree_ies': r['degree_ies'],
                    'nationality': country_br.id if country_br else False,
                })
            else:
                partner = fac.partner_id

            id_map[r['id']] = fac.id
            person_partner_map[r['id']] = partner.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.faculty', fac.id)
            register_xml_id(env, 'universidade_xyzq', f"partner_{r['id']}", 'res.partner', partner.id)
        log(f"  {len(rows)} Docentes cadastrados com sucesso.")

        # ----------------------------------------------------------------------
        # 15. Vínculos Docente-Programa: op.faculty.program.link
        # ----------------------------------------------------------------------
        log("Passo 15: Configurando Vínculos Docente-Programa (op.faculty.program.link)...")
        rows = load_csv('06a_vinculos_docente_programa_op_faculty_program_link.csv')
        for r in rows:
            f_id = id_map[r['faculty_id/id']]
            l_type = r.get('link_type', 'internal')
            p_id = id_map.get(r.get('program_id/id')) if l_type == 'internal' and r.get('program_id/id') else False
            ext_ies = r.get('external_ies_name', '')
            ext_prog = r.get('external_program_name', '')
            ext_snpg = r.get('external_snpg_code', '')
            cat = r.get('faculty_category', 'permanent')
            hours = int(r.get('weekly_hours', 10))

            if l_type == 'internal':
                link = env['op.faculty.program.link'].search([
                    ('faculty_id', '=', f_id),
                    ('link_type', '=', 'internal'),
                    ('program_id', '=', p_id)
                ], limit=1)
            else:
                link = env['op.faculty.program.link'].search([
                    ('faculty_id', '=', f_id),
                    ('link_type', '=', 'external'),
                    ('external_program_name', '=', ext_prog)
                ], limit=1)

            if not link:
                link = env['op.faculty.program.link'].create({
                    'faculty_id': f_id,
                    'link_type': l_type,
                    'program_id': p_id,
                    'external_ies_name': ext_ies,
                    'external_program_name': ext_prog,
                    'external_snpg_code': ext_snpg,
                    'faculty_category': cat,
                    'weekly_hours': hours,
                })
            else:
                link.write({
                    'faculty_category': cat,
                    'weekly_hours': hours,
                    'external_ies_name': ext_ies if l_type == 'external' else False,
                    'external_program_name': ext_prog if l_type == 'external' else False,
                    'external_snpg_code': ext_snpg if l_type == 'external' else False,
                })
            id_map[r['id']] = link.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.faculty.program.link', link.id)
        log(f"  {len(rows)} Vínculos Docente-Programa configurados.")

        # ----------------------------------------------------------------------
        # 16. Livro-Razão de Credenciamento Docente: op.faculty.category.ledger
        # ----------------------------------------------------------------------
        log("Passo 16: Configurando Livro-Razão de Credenciamento Docente (op.faculty.category.ledger)...")
        rows = load_csv('06b_credenciamento_docente_ledger_op_faculty_category_ledger.csv')
        for r in rows:
            pl_id = id_map[r['program_link_id/id']]
            f_led = env['op.faculty.category.ledger'].search([('program_link_id', '=', pl_id), ('category', '=', r['category'])], limit=1)
            if not f_led:
                f_led = env['op.faculty.category.ledger'].create({
                    'program_link_id': pl_id,
                    'category': r['category'],
                    'start_date': r['start_date'],
                    'end_date': r['end_date'] if r['end_date'] else False,
                    'document_ref': r['document_ref'],
                    'notes': r['notes'],
                })
            id_map[r['id']] = f_led.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.faculty.category.ledger', f_led.id)
        log(f"  {len(rows)} Credenciamentos registrados no Livro-Razão.")

        # ----------------------------------------------------------------------
        # 17. Disciplinas do Catálogo: op.subject
        # ----------------------------------------------------------------------
        log("Passo 17: Configurando Disciplinas (op.subject)...")
        rows = load_csv('07a_disciplinas_catalogo_op_subject.csv')
        for r in rows:
            p_id = id_map[r['program_id/id']]
            sub = env['op.subject'].search([('code', '=', r['code'])], limit=1)
            credits_val = float(r['grade_weightage'])
            if not sub:
                sub = env['op.subject'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'type': r['type'],
                    'subject_type': r['subject_type'],
                    'program_id': p_id,
                    'grade_weightage': credits_val,
                    'credits': credits_val,
                })
            id_map[r['id']] = sub.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.subject', sub.id)
        log(f"  {len(rows)} Disciplinas cadastradas no catálogo.")

        # ----------------------------------------------------------------------
        # 18. Regras Curriculares: op.curriculum.subject.rule
        # ----------------------------------------------------------------------
        log("Passo 18: Configurando Regras Curriculares (op.curriculum.subject.rule)...")
        rows = load_csv('07b_regras_curriculares_op_curriculum_subject_rule.csv')
        for r in rows:
            cv_id = id_map[r['curriculum_version_id/id']]
            s_id = id_map[r['subject_id/id']]
            rule = env['op.curriculum.subject.rule'].search([('curriculum_version_id', '=', cv_id), ('subject_id', '=', s_id)], limit=1)
            if not rule:
                rule = env['op.curriculum.subject.rule'].create({
                    'curriculum_version_id': cv_id,
                    'subject_id': s_id,
                    'area_name': r['area_name'],
                    'scope': r['scope'],
                })
            id_map[r['id']] = rule.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.curriculum.subject.rule', rule.id)
        log(f"  {len(rows)} Regras Curriculares configuradas.")

        # ----------------------------------------------------------------------
        # 19. Projetos de Pesquisa: capes.research.project
        # ----------------------------------------------------------------------
        log("Passo 19: Configurando Projetos de Pesquisa (capes.research.project)...")
        rows = load_csv('07c_projetos_pesquisa_capes_research_project.csv')
        for r in rows:
            prog_id = id_map[r['program_id/id']]
            coord_id = id_map[r['coordinator_id/id']]
            line_id = id_map[r['research_line_id/id']]
            proj = env['capes.research.project'].search([('name', '=', r['name']), ('program_id', '=', prog_id)], limit=1)
            if not proj:
                proj = env['capes.research.project'].create({
                    'name': r['name'],
                    'program_id': prog_id,
                    'coordinator_id': coord_id,
                    'research_line_id': line_id,
                    'research_nature': r['research_nature'],
                    'project_type': 'scientific',
                    'funding_agency': r['funding_agency'],
                    'funding_process': r['funding_process'],
                    'start_date': r['start_date'],
                    'end_date': r['end_date'] if r['end_date'] else False,
                    'status': r['status'],
                    'description': r['description'],
                })
            id_map[r['id']] = proj.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.research.project', proj.id)
        log(f"  {len(rows)} Projetos de Pesquisa configurados.")

        # ----------------------------------------------------------------------
        # 20. Editais de Seleção: op.admission.edital
        # ----------------------------------------------------------------------
        log("Passo 20: Configurando Editais de Seleção (op.admission.edital)...")
        rows = load_csv('08_editais_selecao_op_admission_edital.csv')
        for r in rows:
            cv_id = id_map[r['curriculum_version_id/id']]
            ed = env['op.admission.edital'].search([('code', '=', r['code'])], limit=1)
            if not ed:
                ed = env['op.admission.edital'].create({
                    'name': r['name'],
                    'code': r['code'],
                    'curriculum_version_id': cv_id,
                    'academic_year': int(r['academic_year']),
                    'academic_term': '1',
                    'total_slots': int(r['total_slots']),
                    'start_date': r['start_date'],
                    'end_date': r['end_date'],
                    'affirmative_action_percent': float(r['affirmative_action_percent']),
                    'state': r['state'],
                })
            id_map[r['id']] = ed.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.admission.edital', ed.id)
        log(f"  {len(rows)} Editais de Seleção configurados.")

        # ----------------------------------------------------------------------
        # 21. Discentes: op.student & res.partner
        # ----------------------------------------------------------------------
        log("Passo 21: Cadastrando 85 Discentes com Censo CAPES e Integridade...")
        rows = load_csv('09_discentes_identidade_op_student.csv')
        for r in rows:
            st = env['res.country.state'].search([('code', '=', r['birth_state']), ('country_id', '=', country_br.id)], limit=1) or state_sp
            stu = env['op.student'].search([('gr_no', '=', r['gr_no'])], limit=1)
            comp_id = id_map.get(r['company_id/id'], company.id)
            adv_id = id_map.get(r['advisor_id/id']) if r.get('advisor_id/id') else False
            coadv_id = id_map.get(r['coadvisor_id/id']) if r.get('coadvisor_id/id') else False

            if not stu:
                partner = env['res.partner'].create({
                    'name': r['name'],
                    'email': r['email'],
                    'phone': r['phone'],
                    'street': r['street'],
                    'city': r['city'],
                    'zip': r['zip'],
                    'country_id': country_br.id if country_br else False,
                    'state_id': st.id if st else False,
                    'cpf': r['cpf'],
                    'mother_name': r['mother_name'],
                    'race_color': r['race_color'],
                    'has_disability': r['has_disability'].lower() == 'true',
                    'birth_city_name': r['birth_city_name'],
                    'birth_state': r['birth_state'],
                    'orcid': r['orcid'],
                    'lattes_url': r['lattes_url'],
                    'is_company': False,
                })
                stu = env['op.student'].create({
                    'partner_id': partner.id,
                    'first_name': r['first_name'],
                    'middle_name': r['middle_name'],
                    'last_name': r['last_name'],
                    'gender': r['gender'],
                    'birth_date': r['birth_date'],
                    'gr_no': r['gr_no'],
                    'ra_number': r['ra_number'],
                    'company_id': comp_id,
                    'student_category': r['student_category'],
                    'capes_status': r['capes_status'],
                    'admission_date': r['admission_date'],
                    'nationality': country_br.id if country_br else False,
                    'highest_degree': r['highest_degree'],
                    'academic_level': r['academic_level'],
                    'advisor_id': adv_id,
                    'coadvisor_id': coadv_id,
                    'english_proficiency_status': r['english_proficiency_status'],
                    'portuguese_proficiency_status': r['portuguese_proficiency_status'],
                })
            else:
                partner = stu.partner_id

            id_map[r['id']] = stu.id
            person_partner_map[r['id']] = partner.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.student', stu.id)
            register_xml_id(env, 'universidade_xyzq', f"partner_{r['id']}", 'res.partner', partner.id)
        log(f"  {len(rows)} Discentes cadastrados com sucesso.")

        # ----------------------------------------------------------------------
        # 22. Vínculos de Curso: op.student.course
        # ----------------------------------------------------------------------
        log("Passo 22: Configurando Vínculos de Curso (op.student.course)...")
        rows = load_csv('10a_vinculos_curso_op_student_course.csv')
        for r in rows:
            s_id = id_map[r['student_id/id']]
            c_id = id_map[r['course_id/id']]
            b_id = id_map[r['batch_id/id']]
            p_id = id_map[r['program_id/id']]
            cv_id = id_map[r['curriculum_version_id/id']]

            sc = env['op.student.course'].search([('student_id', '=', s_id), ('course_id', '=', c_id)], limit=1)
            if not sc:
                sc = env['op.student.course'].create({
                    'student_id': s_id,
                    'course_id': c_id,
                    'batch_id': b_id,
                    'program_id': p_id,
                    'curriculum_version_id': cv_id,
                    'course_type': r['course_type'],
                    'state': r['state'],
                    'admission_date': r['admission_date'],
                    'completion_date': r['completion_date'] if r['completion_date'] else False,
                })
            env['op.student'].browse(s_id).write({
                'program_id': p_id,
                'curriculum_version_id': cv_id,
            })
            id_map[r['id']] = sc.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.student.course', sc.id)
        log(f"  {len(rows)} Vínculos de Curso configurados.")

        # ----------------------------------------------------------------------
        # 23. Planos de Trabalho: op.student.work_plan
        # ----------------------------------------------------------------------
        log("Passo 23: Configurando Planos de Trabalho (op.student.work_plan)...")
        rows = load_csv('10b_planos_trabalho_op_student_work_plan.csv')
        for r in rows:
            s_id = id_map[r['student_id/id']]
            line_id = id_map[r['research_line_id/id']]
            stu_rec = env['op.student'].browse(s_id)

            wp = env['op.student.work_plan'].search([('student_id', '=', s_id)], limit=1)
            if not wp:
                wp = env['op.student.work_plan'].create({
                    'name': r['name'],
                    'student_id': s_id,
                    'research_line_id': line_id,
                    'research_line': r['research_line'],
                    'summary': r['summary'],
                    'methodology': r['methodology'],
                    'attachment_pdf': r['attachment_pdf'],
                    'opinion_category': r['opinion_category'],
                    'state': r['state'],
                    'cep_approved': True,
                    'advisor_id': stu_rec.advisor_id.id if stu_rec.advisor_id else False,
                })
            id_map[r['id']] = wp.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.student.work_plan', wp.id)
        log(f"  {len(rows)} Planos de Trabalho configurados.")

        # ----------------------------------------------------------------------
        # 24. Livro-Razão Acadêmico Discente: op.student.credit.ledger
        # ----------------------------------------------------------------------
        log("Passo 24: Configurando Livro-Razão Acadêmico de Créditos (op.student.credit.ledger)...")
        rows = load_csv('11_livro_razao_historico_op_student_credit_ledger.csv')
        created_ledgers = 0
        for r in rows:
            s_id = id_map[r['student_id/id']]
            cv_id = id_map[r['curriculum_version_id/id']]
            sub_id = id_map.get(r['subject_id/id']) if r.get('subject_id/id') else False

            led = env['op.student.credit.ledger'].search([
                ('student_id', '=', s_id),
                ('course_name', '=', r['course_name']),
                ('date_earned', '=', r['date_earned'])
            ], limit=1)

            if not led:
                led = env['op.student.credit.ledger'].create({
                    'student_id': s_id,
                    'curriculum_version_id': cv_id,
                    'subject_id': sub_id,
                    'course_name': r['course_name'],
                    'credit_type': r['credit_type'],
                    'credits': float(r['credits']),
                    'hours': float(r['hours']) if r.get('hours') else 0.0,
                    'grade_concept': r['grade_concept'] if r.get('grade_concept') else False,
                    'is_approved': r['is_approved'].lower() == 'true',
                    'date_earned': r['date_earned'],
                    'origin_ref': r['origin_ref'],
                })
                created_ledgers += 1
            id_map[r['id']] = led.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.student.credit.ledger', led.id)
        log(f"  {len(rows)} Registros no Livro-Razão auditados ({created_ledgers} criados).")

        # ----------------------------------------------------------------------
        # 25. Defesas e Ritos de Tese: capes.thesis
        # ----------------------------------------------------------------------
        log("Passo 25: Configurando Defesas de Tese e Ritos Finais (capes.thesis)...")
        rows = load_csv('12a_bancas_defesas_capes_thesis.csv')
        for r in rows:
            s_id = id_map[r['student_id/id']]
            wp_id = id_map[r['work_plan_id/id']]

            th = env['capes.thesis'].search([('student_id', '=', s_id)], limit=1)
            if not th:
                th = env['capes.thesis'].create({
                    'student_id': s_id,
                    'work_plan_id': wp_id,
                    'title': r['title'],
                    'doc_type': r['doc_type'],
                    'stage': r['stage'],
                    'status': r['status'],
                    'defense_date': r['defense_date'],
                    'repository_url': r['repository_url'],
                    'secretariat_approval': True,
                    'secretariat_approval_date': r['defense_date'][:10],
                })
            id_map[r['id']] = th.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.thesis', th.id)
        log(f"  {len(rows)} Defesas de Tese cadastradas.")

        # ----------------------------------------------------------------------
        # 26. Comissões Examinadoras (Bancas): capes.thesis.committee
        # ----------------------------------------------------------------------
        log("Passo 26: Configurando Membros das Comissões Examinadoras (capes.thesis.committee)...")
        rows = load_csv('12b_comissoes_examinadoras_capes_thesis_committee.csv')
        for r in rows:
            th_id = id_map[r['thesis_id/id']]
            mem_partner_id = person_partner_map[r['member_id/id']]

            comm = env['capes.thesis.committee'].search([('thesis_id', '=', th_id), ('member_id', '=', mem_partner_id)], limit=1)
            if not comm:
                comm = env['capes.thesis.committee'].create({
                    'thesis_id': th_id,
                    'member_id': mem_partner_id,
                    'member_role': r['member_role'],
                    'is_titular': r['is_titular'].lower() == 'true',
                })
            id_map[r['id']] = comm.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.thesis.committee', comm.id)
        log(f"  {len(rows)} Membros de Comissões Examinadoras configurados.")

        # ----------------------------------------------------------------------
        # 27. Produtos PTT: capes.ptt.product
        # ----------------------------------------------------------------------
        log("Passo 27: Configurando Produtos PTT Tecnológicos (capes.ptt.product)...")
        rows = load_csv('13a_produtos_ptt_capes_ptt_product.csv')
        for r in rows:
            th_id = id_map[r['thesis_id/id']]
            s_id = id_map[r['student_id/id']]
            type_rec = env.ref(r['type_id/id'])

            ptt = env['capes.ptt.product'].search([('thesis_id', '=', th_id)], limit=1)
            if not ptt:
                ptt = env['capes.ptt.product'].create({
                    'title': r['title'],
                    'thesis_id': th_id,
                    'student_id': s_id,
                    'type_id': type_rec.id,
                    'axis_id': type_rec.axis_id.id if type_rec.axis_id else False,
                    'final_stratum': r['final_stratum'],
                    'trl_level': r['trl_level'],
                    'adherence_justif': r['adherence_justif'],
                    'state': r['state'],
                })
            id_map[r['id']] = ptt.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.ptt.product', ptt.id)
        log(f"  {len(rows)} Produtos PTT configurados.")

        # ----------------------------------------------------------------------
        # 28. Coautores PTT: capes.ptt.author
        # ----------------------------------------------------------------------
        log("Passo 28: Configurando Coautores de Produtos PTT (capes.ptt.author)...")
        rows = load_csv('13b_autores_ptt_capes_ptt_author.csv')
        for r in rows:
            prod_id = id_map[r['product_id/id']]
            auth_partner_id = person_partner_map[r['partner_id/id']]

            auth = env['capes.ptt.author'].search([('product_id', '=', prod_id), ('partner_id', '=', auth_partner_id)], limit=1)
            if not auth:
                auth = env['capes.ptt.author'].create({
                    'product_id': prod_id,
                    'partner_id': auth_partner_id,
                    'author_role': r['author_role'],
                    'ip_share': float(r['ip_share']),
                })
            id_map[r['id']] = auth.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.ptt.author', auth.id)
        log(f"  {len(rows)} Coautores PTT vinculados.")

        # ----------------------------------------------------------------------
        # 29. Diplomas Digitais: capes.digital.diploma
        # ----------------------------------------------------------------------
        log("Passo 29: Configurando Diplomas Digitais Soberanos (capes.digital.diploma)...")
        rows = load_csv('14_diplomas_digitais_capes_digital_diploma.csv')
        for r in rows:
            s_id = id_map[r['student_id/id']]
            th_id = id_map[r['thesis_id/id']]

            dip = env['capes.digital.diploma'].search([('thesis_id', '=', th_id)], limit=1)
            if not dip:
                dip = env['capes.digital.diploma'].create({
                    'student_id': s_id,
                    'thesis_id': th_id,
                    'degree_type': r['degree_type'],
                    'issuing_ies_type': r['issuing_ies_type'],
                    'emission_format': r['emission_format'],
                    'origin_ies_name': r['origin_ies_name'],
                    'issuing_ies_name': r['issuing_ies_name'],
                    'diploma_process_number': r['diploma_process_number'],
                    'registration_book_number': r['registration_book_number'],
                    'registration_page_number': r['registration_page_number'],
                    'graduation_date': r['graduation_date'],
                    'registration_date': r['registration_date'] if r['registration_date'] else False,
                    'state': r['state'],
                })
            id_map[r['id']] = dip.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'capes.digital.diploma', dip.id)
        log(f"  {len(rows)} Diplomas Digitais registrados.")

        # ----------------------------------------------------------------------
        # 30. Governança CPG - Comissões: op.cpg.committee
        # ----------------------------------------------------------------------
        log("Passo 30: Configurando Comissões CPG (op.cpg.committee)...")
        rows = load_csv('15a_governanca_cpg_comissoes_op_cpg_committee.csv')
        for r in rows:
            p_id = id_map[r['program_id/id']]
            cpg = env['op.cpg.committee'].search([('program_id', '=', p_id)], limit=1)
            if not cpg:
                cpg = env['op.cpg.committee'].create({
                    'name': r['name'],
                    'program_id': p_id,
                    'start_date': r['start_date'],
                    'end_date': r['end_date'] if r['end_date'] else False,
                    'status': r['status'],
                })
            id_map[r['id']] = cpg.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.cpg.committee', cpg.id)
        log(f"  {len(rows)} Comissões CPG configuradas.")

        # ----------------------------------------------------------------------
        # 31. Governança CPG - Membros: op.cpg.member
        # ----------------------------------------------------------------------
        log("Passo 31: Configurando Membros das Comissões CPG (op.cpg.member)...")
        rows = load_csv('15b_membros_cpg_op_cpg_member.csv')
        for r in rows:
            comm_id = id_map[r['committee_id/id']]
            mem_partner_id = person_partner_map[r['partner_id/id']]

            mem = env['op.cpg.member'].search([('committee_id', '=', comm_id), ('partner_id', '=', mem_partner_id)], limit=1)
            if not mem:
                mem = env['op.cpg.member'].create({
                    'committee_id': comm_id,
                    'partner_id': mem_partner_id,
                    'role': r['role'],
                    'mandate_origin': r['mandate_origin'],
                    'document_ref': r['document_ref'],
                })
            id_map[r['id']] = mem.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.cpg.member', mem.id)
        log(f"  {len(rows)} Membros CPG vinculados.")

        # ----------------------------------------------------------------------
        # 32. Governança CPG - Reuniões e Atas: op.cpg.meeting
        # ----------------------------------------------------------------------
        log("Passo 32: Configurando Reuniões e Atas CPG (op.cpg.meeting)...")
        rows = load_csv('15c_reunioes_atas_cpg_op_cpg_meeting.csv')
        for r in rows:
            comm_id = id_map[r['committee_id/id']]
            meet = env['op.cpg.meeting'].search([('committee_id', '=', comm_id), ('meeting_date', '=', r['meeting_date'])], limit=1)
            if not meet:
                meet = env['op.cpg.meeting'].create({
                    'name': r['name'],
                    'committee_id': comm_id,
                    'meeting_date': r['meeting_date'],
                    'meeting_type': r['meeting_type'],
                    'state': r['state'],
                })
            id_map[r['id']] = meet.id
            register_xml_id(env, 'universidade_xyzq', r['id'], 'op.cpg.meeting', meet.id)
        log(f"  {len(rows)} Reuniões e Atas CPG registradas.")

        # ----------------------------------------------------------------------
        # 33. Usuários e Perfis de Acesso: res.users
        # ----------------------------------------------------------------------
        log("Passo 33: Configurando Usuários e Perfis de Acesso (res.users)...")
        g_user = env.ref('base.group_user')
        g_admin = env.ref('openeducat_core.group_op_back_office_admin')
        g_fac = env.ref('openeducat_core.group_op_faculty')
        g_sys = env.ref('base.group_system')
        g_capes_admin = env.ref('l10n_br_openeducat_capes_core.group_capes_central_admin')
        g_capes_coord = env.ref('l10n_br_openeducat_capes_core.group_capes_program_coordinator')
        g_capes_sec = env.ref('l10n_br_openeducat_capes_core.group_capes_program_secretary')

        p_cc = id_map['prog_xyzq_cc']
        p_fis = id_map['prog_xyzq_fis']
        p_bio = id_map['prog_xyzq_bio']
        p_mpesi = id_map['prog_xyzq_mpe']
        all_p = [p_cc, p_fis, p_bio, p_mpesi]

        user_admin = env['res.users'].browse(SUPERUSER_ID)
        user_admin.write({
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
            'is_central_admin': True,
            'allowed_program_ids': [(6, 0, all_p)],
            'current_program_id': p_cc,
        })
        admin_rec = env['res.users'].search([('login', '=', 'admin')], limit=1)
        if admin_rec:
            admin_rec.write({
                'company_id': company.id,
                'company_ids': [(6, 0, [company.id])],
                'is_central_admin': True,
                'allowed_program_ids': [(6, 0, all_p)],
                'current_program_id': p_cc,
            })

        user_configs = [
            ('admin_xyzq', 'Administrador Geral XYZQ', 'admin.posgrad@xyzq.edu.br', 'xyzq123', None, [g_user, g_admin, g_sys, g_capes_admin], True, all_p, p_cc),
            ('secretaria_xyzq', 'Secretaria Multi-Programa (CC e MPESI)', 'sec.posgrad@xyzq.edu.br', 'secretaria123', None, [g_user, g_admin, g_capes_sec], False, [p_cc, p_mpesi], p_cc),
            ('secretaria', 'Secretaria Setorial PPGCC', 'secretaria@xyzq.edu.br', 'secretaria123', None, [g_user, g_admin, g_capes_sec], False, [p_cc], p_cc),
            ('coord_ppgcc', 'Prof. Dr. André Soares Muniz (Coord. PPGCC)', 'coord.ppgcc@xyzq.edu.br', 'coordenador123', person_partner_map.get('fac_xyzq_01'), [g_user, g_admin, g_fac, g_capes_coord], False, [p_cc], p_cc),
            ('coordenador', 'Coordenador Geral CPG', 'coordenador@xyzq.edu.br', 'coordenador123', person_partner_map.get('fac_xyzq_01'), [g_user, g_admin, g_fac, g_capes_coord], False, [p_cc], p_cc),
            ('coord_mpesi', 'Prof. Dr. Daniel Nascimento Bueno (Coord. MPESI)', 'coord.mpesi@xyzq.edu.br', 'coordenador123', person_partner_map.get('fac_xyzq_05'), [g_user, g_admin, g_fac, g_capes_coord], False, [p_mpesi], p_mpesi),
            ('prof_xyzq', 'Prof. Dr. Bruno Fernandes Sardenberg (Docente)', 'roberto.docente@xyzq.edu.br', 'professor123', person_partner_map.get('fac_xyzq_03'), [g_user, g_fac], False, [p_cc], p_cc),
            ('professor', 'Docente Permanente CPG', 'professor@xyzq.edu.br', 'professor123', person_partner_map.get('fac_xyzq_03'), [g_user, g_fac], False, [p_cc], p_cc),
        ]

        for login, name, email, pwd, partner_id, groups, is_c_admin, allowed_p, curr_p in user_configs:
            u = env['res.users'].search([('login', '=', login)], limit=1)
            group_ids = [g.id for g in groups]
            if not u:
                vals = {
                    'name': name,
                    'login': login,
                    'email': email,
                    'password': pwd,
                    'company_id': company.id,
                    'company_ids': [(6, 0, [company.id])],
                    'group_ids': [(6, 0, group_ids)],
                    'is_central_admin': is_c_admin,
                    'allowed_program_ids': [(6, 0, allowed_p)],
                    'current_program_id': curr_p,
                }
                if partner_id:
                    vals['partner_id'] = partner_id
                u = env['res.users'].create(vals)
            else:
                write_vals = {
                    'company_id': company.id,
                    'company_ids': [(6, 0, [company.id])],
                    'password': pwd,
                    'group_ids': [(4, gid) for gid in group_ids],
                    'is_central_admin': is_c_admin,
                    'allowed_program_ids': [(6, 0, allowed_p)],
                    'current_program_id': curr_p,
                }
                if partner_id:
                    write_vals['partner_id'] = partner_id
                u.write(write_vals)
            log(f"  Usuário '{login}' configurado com sucesso (Senha: {pwd}).")


        # ----------------------------------------------------------------------
        # 34. Módulo de Bolsas CAPES: Edital, Cota e Inscrições Demonstrativas
        # ----------------------------------------------------------------------
        log("Passo 34: Configurando Dados Demonstrativos de Bolsas CAPES (l10n_br_openeducat_capes_scholarship)...")
        crs_cc_id = id_map.get('crs_xyzq_cc')
        ay_2024_id = id_map.get('ay_xyzq_2024')
        sponsor_capes = env.ref('l10n_br_openeducat_capes_scholarship.sponsor_capes', raise_if_not_found=False)
        rubric_me = env.ref('l10n_br_openeducat_capes_scholarship.rubric_ipen_master_acad', raise_if_not_found=False)

        if crs_cc_id and ay_2024_id and sponsor_capes and rubric_me:
            quota = env['capes.scholarship.quota'].search([('course_id', '=', crs_cc_id), ('sponsor_id', '=', sponsor_capes.id)], limit=1)
            if not quota:
                quota = env['capes.scholarship.quota'].create({
                    'name': 'Cota CAPES/DS Mestrado PPGCC 2024',
                    'sponsor_id': sponsor_capes.id,
                    'course_id': crs_cc_id,
                    'program_id': p_cc,
                    'level': 'master_acad',
                    'total_slots': 5,
                    'validity_start': '2024-01-01',
                    'validity_end': '2026-12-31',
                    'monthly_reference_amount': 2100.00,
                })
            log(f"  Cota de Bolsas configurada: {quota.name} ({quota.total_slots} vagas)")

            edital_bolsa = env['capes.scholarship.edital'].search([('name', '=', 'Edital de Bolsas PPGCC 01/2024')], limit=1)
            if not edital_bolsa:
                edital_bolsa = env['capes.scholarship.edital'].create({
                    'name': 'Edital de Bolsas PPGCC 01/2024',
                    'course_id': crs_cc_id,
                    'program_id': p_cc,
                    'academic_year_id': ay_2024_id,
                    'quota_id': quota.id,
                    'rubric_id': rubric_me.id,
                    'slots_total': 5,
                    'slots_open_competition': 4,
                    'slots_affirmative_action': 1,
                    'date_start': '2024-02-01',
                    'date_end': '2024-03-15',
                    'date_preliminary_result': '2024-03-20 18:00:00',
                    'date_appeals_end': '2024-03-25 18:00:00',
                    'date_final_result': '2024-03-30 18:00:00',
                    'state': 'open',
                })
            log(f"  Edital de Bolsa configurado: ID={edital_bolsa.id} ({edital_bolsa.name})")

            # Inscrição de Aluno em Bolsa
            stu_cand = env['op.student'].search([('gr_no', '=', 'RA20241001')], limit=1)
            fac_rev1 = env['op.faculty'].search([], limit=1)
            fac_rev2 = env['op.faculty'].search([('id', '!=', fac_rev1.id)], limit=1)
            if stu_cand and fac_rev1:
                app = env['capes.scholarship.application'].search([('edital_id', '=', edital_bolsa.id), ('student_id', '=', stu_cand.id)], limit=1)
                if not app:
                    app = env['capes.scholarship.application'].create({
                        'edital_id': edital_bolsa.id,
                        'student_id': stu_cand.id,
                        'faculty_id': stu_cand.advisor_id.id if stu_cand.advisor_id else fac_rev1.id,
                        'reviewer1_id': fac_rev1.id,
                        'reviewer2_id': fac_rev2.id if fac_rev2 else False,
                        'lattes_url': 'http://lattes.cnpq.br/855274516000002',
                        'quota_type': 'ampla',
                        'dedication_mode': 'exclusive',
                        'state': 'under_review',
                    })
                log(f"  Inscrição em bolsa demonstrativa criada para o discente {stu_cand.name} (Protocolo: {app.name})")

        cr.commit()
        log("=========================================================================")
        log("CARGA DO CENÁRIO UNIVERSIDADE XYZQ CONCLUÍDA COM 100% DE SUCESSO!")
        log(f"Banco de Dados: {DB_NAME}")
        log("4 Programas CAPES carregados com 25 Docentes, 85 Discentes, Bancas, PTT, Diplomas e Bolsas.")
        log("=========================================================================")

if __name__ == '__main__':
    run_import()
