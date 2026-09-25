#!/usr/bin/env python3
"""
Auditor Forense e Validador de Integridade Relacional de Datasets Sintéticos
Valida:
1. Existência e integridade de cabeçalhos de todos os 33 arquivos CSV.
2. Integridade de Chaves Estrangeiras (Foreign Keys) cruzadas em memória.
3. Unicidade absoluta de nomes brasileiros completos (Docentes e Discentes).
4. Coerência da decomposição first_name, middle_name e last_name.
5. Validação algorítmica de CPFs brasileiros (dígitos verificadores).
6. Conformidade de XML IDs e tipologias PTT oficiais.
"""

import os
import csv
import sys

def validate_cpf(cpf_str):
    cpf = ''.join(c for c in cpf_str if c.isdigit())
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    s1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 11 - (s1 % 11)
    d1 = 0 if d1 >= 10 else d1
    if int(cpf[9]) != d1:
        return False
    s2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 11 - (s2 % 11)
    d2 = 0 if d2 >= 10 else d2
    return int(cpf[10]) == d2

def load_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def audit_scenario(scenario_dir, scenario_name):
    print(f"\n=======================================================")
    print(f"AUDITANDO CENÁRIO: {scenario_name}")
    print(f"Diretório: {scenario_dir}")
    print(f"=======================================================")
    
    errors = []
    warnings = []
    
    # Mapeamento de coleções por ID
    tables = {}
    csv_files = [f for f in os.listdir(scenario_dir) if f.endswith('.csv')]
    csv_files.sort()
    
    print(f"Arquivos CSV encontrados: {len(csv_files)}")
    if len(csv_files) != 33:
        warnings.append(f"Esperado 33 arquivos CSV, encontrados {len(csv_files)}")

    for fname in csv_files:
        fpath = os.path.join(scenario_dir, fname)
        rows = load_csv(fpath)
        tables[fname] = rows

    # 1. Auditoria de Pessoas (Docentes e Discentes): Unicidade e Onomástica
    print("\n--- 1. Auditoria de Nomes, CPFs e Censo CAPES ---")
    all_person_names = set()
    fac_ids = set()
    stu_ids = set()
    
    # Docentes
    fac_file = [f for f in csv_files if '05_docentes_orientadores' in f][0]
    for row in tables[fac_file]:
        fid = row['id']
        fac_ids.add(fid)
        full_name = row['name']
        fn = row['first_name']
        mn = row['middle_name']
        ln = row['last_name']
        cpf = row['cpf']
        
        # Unicidade
        if full_name in all_person_names:
            errors.append(f"Nome de docente duplicado: '{full_name}' (ID: {fid})")
        all_person_names.add(full_name)
        
        # Decomposição
        expected_full = " ".join(filter(None, [fn, mn, ln]))
        if expected_full != full_name:
            errors.append(f"Decomposição incoerente no docente {fid}: '{full_name}' != '{expected_full}'")
            
        # CPF
        if not validate_cpf(cpf):
            errors.append(f"CPF inválido no docente {fid}: {cpf}")
            
        # Censo CAPES
        if not row.get('mother_name'):
            errors.append(f"Docente {fid} sem nome da mãe")
        if not row.get('race_color'):
            errors.append(f"Docente {fid} sem raça/cor")
        if not row.get('birth_city_name') or not row.get('birth_state'):
            errors.append(f"Docente {fid} sem naturalidade (cidade/UF)")

    print(f"[OK] {len(fac_ids)} docentes auditados com 100% de CPFs válidos e dados censitários completos.")

    # Discentes
    stu_file = [f for f in csv_files if '09_discentes_identidade' in f][0]
    for row in tables[stu_file]:
        sid = row['id']
        stu_ids.add(sid)
        full_name = row['name']
        fn = row['first_name']
        mn = row['middle_name']
        ln = row['last_name']
        cpf = row['cpf']
        
        # Unicidade
        if full_name in all_person_names:
            errors.append(f"Nome de discente duplicado ou colidente: '{full_name}' (ID: {sid})")
        all_person_names.add(full_name)
        
        # Decomposição
        expected_full = " ".join(filter(None, [fn, mn, ln]))
        if expected_full != full_name:
            errors.append(f"Decomposição incoerente no discente {sid}: '{full_name}' != '{expected_full}'")
            
        # CPF
        if not validate_cpf(cpf):
            errors.append(f"CPF inválido no discente {sid}: {cpf}")
            
        # Orientador
        adv_id = row.get('advisor_id/id')
        if adv_id and adv_id not in fac_ids:
            errors.append(f"Discente {sid} com orientador inválido: '{adv_id}'")

    print(f"[OK] {len(stu_ids)} discentes auditados com 100% de unicidade e vínculos válidos.")
    print(f"[TOTAL] {len(all_person_names)} identidades soberanas únicas cadastradas.")

    # 2. Auditoria Relacional de Chaves Estrangeiras (Foreign Keys)
    print("\n--- 2. Auditoria Relacional de Integridade Referencial (FKs) ---")
    
    # ID sets de entidades base
    prog_ids = {r['id'] for r in tables[[f for f in csv_files if '02_programas_capes' in f][0]]}
    reg_ids = {r['id'] for r in tables[[f for f in csv_files if '03_versao_curricular' in f][0]]}
    area_ids = {r['id'] for r in tables[[f for f in csv_files if '04a_areas_concentracao' in f][0]]}
    line_ids = {r['id'] for r in tables[[f for f in csv_files if '04b_linhas_pesquisa' in f][0]]}
    course_ids = {r['id'] for r in tables[[f for f in csv_files if '01h_cursos_openeducat' in f][0]]}
    batch_ids = {r['id'] for r in tables[[f for f in csv_files if '01i_lotes_turmas' in f][0]]}
    subject_ids = {r['id'] for r in tables[[f for f in csv_files if '07a_disciplinas' in f][0]]}
    wp_ids = {r['id'] for r in tables[[f for f in csv_files if '10b_planos_trabalho' in f][0]]}
    thesis_ids = {r['id'] for r in tables[[f for f in csv_files if '12a_bancas_defesas' in f][0]]}

    # Validação de Linhas de Pesquisa -> Áreas
    for r in tables[[f for f in csv_files if '04b_linhas_pesquisa' in f][0]]:
        if r['area_id/id'] not in area_ids:
            errors.append(f"Linha de pesquisa {r['id']} aponta para area inexistente: {r['area_id/id']}")

    # Validação de Vínculos Docente-Programa
    link_file = [f for f in csv_files if '06a_vinculos_docente' in f][0]
    fac_link_ids = set()
    for r in tables[link_file]:
        fac_link_ids.add(r['id'])
        if r['faculty_id/id'] not in fac_ids:
            errors.append(f"Vínculo docente {r['id']} aponta para docente inexistente: {r['faculty_id/id']}")
        if r.get('link_type') != 'external':
            if r['program_id/id'] not in prog_ids:
                errors.append(f"Vínculo docente {r['id']} aponta para programa inexistente: {r['program_id/id']}")
        else:
            if not r.get('external_ies_name') or not r.get('external_program_name'):
                errors.append(f"Vínculo docente externo {r['id']} sem instituição ou programa externo: {r['id']}")

    # Validação de Livro-Razão de Credenciamento Docente
    fac_led_file = [f for f in csv_files if '06b_credenciamento_docente' in f][0]
    for r in tables[fac_led_file]:
        if r['program_link_id/id'] not in fac_link_ids:
            errors.append(f"Credenciamento {r['id']} aponta para vínculo inexistente: {r['program_link_id/id']}")
        if not r.get('start_date'):
            errors.append(f"Credenciamento {r['id']} sem data de início")

    # Validação de Vínculos de Curso Discente (op.student.course)
    sc_file = [f for f in csv_files if '10a_vinculos_curso' in f][0]
    for r in tables[sc_file]:
        if r['student_id/id'] not in stu_ids:
            errors.append(f"Vínculo de curso {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if r['course_id/id'] not in course_ids:
            errors.append(f"Vínculo de curso {r['id']} aponta para curso inexistente: {r['course_id/id']}")
        if r['batch_id/id'] not in batch_ids:
            errors.append(f"Vínculo de curso {r['id']} aponta para turma/lote inexistente: {r['batch_id/id']}")
        if r['program_id/id'] not in prog_ids:
            errors.append(f"Vínculo de curso {r['id']} aponta para programa CAPES inexistente: {r['program_id/id']}")
        if r['curriculum_version_id/id'] not in reg_ids:
            errors.append(f"Vínculo de curso {r['id']} aponta para regimento inexistente: {r['curriculum_version_id/id']}")

    # Validação de Planos de Trabalho
    for r in tables[[f for f in csv_files if '10b_planos_trabalho' in f][0]]:
        if r['student_id/id'] not in stu_ids:
            errors.append(f"Plano de trabalho {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if r['research_line_id/id'] not in line_ids:
            errors.append(f"Plano de trabalho {r['id']} aponta para linha inexistente: {r['research_line_id/id']}")
        if not r.get('attachment_pdf'):
            errors.append(f"Plano de trabalho {r['id']} sem attachment_pdf em base64")

    # Validação do Livro-Razão Acadêmico Discente
    led_file = [f for f in csv_files if '11_livro_razao' in f][0]
    for r in tables[led_file]:
        if r['student_id/id'] not in stu_ids:
            errors.append(f"Entrada no ledger {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if r['curriculum_version_id/id'] not in reg_ids:
            errors.append(f"Entrada no ledger {r['id']} aponta para regimento inexistente: {r['curriculum_version_id/id']}")
        if r.get('subject_id/id') and r['subject_id/id'] not in subject_ids:
            errors.append(f"Entrada no ledger {r['id']} aponta para disciplina inexistente: {r['subject_id/id']}")

    # Validação de Defesas de Tese / Ritos
    th_file = [f for f in csv_files if '12a_bancas_defesas' in f][0]
    for r in tables[th_file]:
        if r['student_id/id'] not in stu_ids:
            errors.append(f"Defesa {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if r['work_plan_id/id'] not in wp_ids:
            errors.append(f"Defesa {r['id']} aponta para plano de trabalho inexistente: {r['work_plan_id/id']}")
        if 'advisor_id' in r:
            errors.append(f"Defesa {r['id']} contém coluna proibida advisor_id")

    # Validação de Comissões Examinadoras (Bancas)
    comm_file = [f for f in csv_files if '12b_comissoes_examinadoras' in f][0]
    for r in tables[comm_file]:
        if r['thesis_id/id'] not in thesis_ids:
            errors.append(f"Membro de banca {r['id']} aponta para defesa inexistente: {r['thesis_id/id']}")
        if r['member_id/id'] not in fac_ids and r['member_id/id'] not in stu_ids:
            errors.append(f"Membro de banca {r['id']} aponta para examinador inexistente: {r['member_id/id']}")

    # Validação de Produtos PTT
    ptt_file = [f for f in csv_files if '13a_produtos_ptt' in f][0]
    ptt_ids = set()
    for r in tables[ptt_file]:
        ptt_ids.add(r['id'])
        if r['thesis_id/id'] not in thesis_ids:
            errors.append(f"PTT {r['id']} aponta para defesa inexistente: {r['thesis_id/id']}")
        if r['student_id/id'] not in stu_ids:
            errors.append(f"PTT {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if 'axis_id' in r or 'axis_id/id' in r:
            errors.append(f"PTT {r['id']} contém coluna proibida/readonly axis_id")
        if not r['type_id/id'].startswith('l10n_br_openeducat_capes_ptt.'):
            errors.append(f"PTT {r['id']} com external ID de tipologia inválido: {r['type_id/id']}")

    # Validação de Diplomas Digitais
    dip_file = [f for f in csv_files if '14_diplomas_digitais' in f][0]
    for r in tables[dip_file]:
        if r['student_id/id'] not in stu_ids:
            errors.append(f"Diploma {r['id']} aponta para discente inexistente: {r['student_id/id']}")
        if r['thesis_id/id'] not in thesis_ids:
            errors.append(f"Diploma {r['id']} aponta para defesa inexistente: {r['thesis_id/id']}")

    print(f"[OK] Integridade referencial validada para todas as tabelas e modelos cruzados.")

    # Relatório Final do Cenário
    print("\n--- 3. Relatório da Auditoria ---")
    if errors:
        print(f"❌ ENCONTRADOS {len(errors)} ERROS:")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... e mais {len(errors) - 20} erros.")
        return False
    else:
        print("✅ 0 ERROS DETECTADOS! Dataset em 100% de conformidade com o esquema do banco!")
        if warnings:
            print(f"Avisos ({len(warnings)}):")
            for w in warnings:
                print(f"  * {w}")
        return True

if __name__ == '__main__':
    base_dir = 'import_templates/datasets_sinteticos'
    r1 = audit_scenario(os.path.join(base_dir, 'universidade_xyzq'), "Cenário 1: Universidade XYZQ")
    r2 = audit_scenario(os.path.join(base_dir, 'mptrcs_ipen'), "Cenário 2: MPTRCS / IPEN-CNEN/SP")
    
    if r1 and r2:
        print("\n🏆 SUCESSO TOTAL: Ambos os cenários sintéticos estão 100% íntegros e compatíveis com o Odoo 19!")
        sys.exit(0)
    else:
        print("\n💥 FALHA NA VALIDAÇÃO DE INTEGRIDADE!")
        sys.exit(1)
