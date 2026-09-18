#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_multiprogram_isolation.py
Validação automatizada de isolamento multiprograma, segurança e alternância contextual (Opção B).
Testa os bancos 'universidade_xyzq' e 'mptrcs_ipen_prod'.
"""
import sys
import logging

import odoo
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("test_multiprogram_isolation")
CONFIG_PATH = '/etc/odoo/odoo.conf'

def test_xyzq_isolation():
    log.info("=== TESTANDO ISOLAMENTO EM 'universidade_xyzq' ===")
    odoo.tools.config.parse_config(['-c', CONFIG_PATH, '-d', 'universidade_xyzq', '--no-http'])
    registry = Registry('universidade_xyzq')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Obter programas
        programs = env['op.program.capes'].search([])
        prog_map = {p.short_name: p.id for p in programs}
        log.info(f"Programas existentes no banco: {list(prog_map.keys())}")
        assert len(prog_map) == 4, f"Esperado 4 programas, encontrados {len(prog_map)}"

        # 1. Testar Administrador Central (admin_xyzq)
        user_admin = env['res.users'].search([('login', '=', 'admin_xyzq')], limit=1)
        assert user_admin, "Usuário admin_xyzq não encontrado!"
        env_admin = api.Environment(cr, user_admin.id, {})

        admin_progs = env_admin['op.program.capes'].search([])
        log.info(f"[admin_xyzq] Programas visíveis: {len(admin_progs)}")
        assert len(admin_progs) == 4, f"admin_xyzq deveria ver 4 programas, viu {len(admin_progs)}"

        admin_batches = env_admin['op.batch'].search([])
        log.info(f"[admin_xyzq] Turmas visíveis: {len(admin_batches)}")
        assert len(admin_batches) == 4, f"admin_xyzq deveria ver 4 turmas, viu {len(admin_batches)}"

        admin_students = env_admin['op.student'].search([])
        log.info(f"[admin_xyzq] Discentes visíveis: {len(admin_students)}")
        assert len(admin_students) == 85, f"admin_xyzq deveria ver 85 discentes, viu {len(admin_students)}"

        # Testar alternância do admin_xyzq para qualquer programa
        env_admin['res.users'].action_switch_program(prog_map['MPESI'])
        log.info("[admin_xyzq] Alternância de programa testada com sucesso!")

        # 2. Testar Secretaria Multi-Programa (secretaria_xyzq: CC e MPESI)
        user_sec_multi = env['res.users'].search([('login', '=', 'secretaria_xyzq')], limit=1)
        assert user_sec_multi, "Usuário secretaria_xyzq não encontrado!"
        env_sec_multi = api.Environment(cr, user_sec_multi.id, {})

        # Os programas autorizados no dropdown
        sec_multi_progs = env_sec_multi['op.program.capes'].search([])
        sec_multi_prog_names = [p.short_name for p in sec_multi_progs]
        log.info(f"[secretaria_xyzq] Programas autorizados: {sec_multi_prog_names}")
        assert set(sec_multi_prog_names) == {'PPGCC', 'MPESI'}, f"Esperado PPGCC e MPESI, obtido: {sec_multi_prog_names}"

        # 2a. Contexto Ativo 1: PPGCC
        env_sec_step1 = api.Environment(cr, user_sec_multi.id, {})
        prog_cc = env_sec_step1['op.program.capes'].browse(prog_map['PPGCC'])
        prog_cc.action_select_as_current()
        cr.commit()

        env_sec_cc = api.Environment(cr, user_sec_multi.id, {})
        p_cc_check = env_sec_cc['op.program.capes'].browse(prog_map['PPGCC'])
        assert p_cc_check.is_current_program, "PPGCC deveria estar ativo!"
        assert p_cc_check.session_status == 'Programa Ativo', "Status deveria ser Programa Ativo!"

        areas_cc = env_sec_cc['op.program.concentration.area'].search([])
        log.info(f"[secretaria_xyzq @ PPGCC] Áreas de Concentração: {len(areas_cc)}")
        assert len(areas_cc) == 2, f"Deveria ver 2 áreas do PPGCC, viu {len(areas_cc)}"

        lines_cc = env_sec_cc['op.program.research.line'].search([])
        log.info(f"[secretaria_xyzq @ PPGCC] Linhas de Pesquisa: {len(lines_cc)}")
        assert len(lines_cc) == 4, f"Deveria ver 4 linhas do PPGCC, viu {len(lines_cc)}"

        projects_cc = env_sec_cc['capes.research.project'].search([])
        log.info(f"[secretaria_xyzq @ PPGCC] Projetos de Pesquisa: {len(projects_cc)}")
        assert len(projects_cc) == 2, f"Deveria ver 2 projetos do PPGCC, viu {len(projects_cc)}"

        batches_cc = env_sec_cc['op.batch'].search([])
        log.info(f"[secretaria_xyzq @ PPGCC] Turmas visíveis: {len(batches_cc)}")
        assert len(batches_cc) == 1, f"secretaria_xyzq com PPGCC ativo deveria ver 1 turma, viu {len(batches_cc)}"
        students_cc = env_sec_cc['op.student'].search([])
        log.info(f"[secretaria_xyzq @ PPGCC] Discentes visíveis: {len(students_cc)}")
        assert len(students_cc) == 20, f"secretaria_xyzq com PPGCC ativo deveria ver 20 discentes, viu {len(students_cc)}"

        # 2b. Contexto Ativo 2: MPESI (Alternância de Programa via action_select_as_current)
        env_sec_step2 = api.Environment(cr, user_sec_multi.id, {})
        prog_mpe = env_sec_step2['op.program.capes'].browse(prog_map['MPESI'])
        prog_mpe.action_select_as_current()
        cr.commit()

        env_sec_mpe = api.Environment(cr, user_sec_multi.id, {})
        p_mpe_check = env_sec_mpe['op.program.capes'].browse(prog_map['MPESI'])
        assert p_mpe_check.is_current_program, "MPESI deveria estar ativo!"

        areas_mpe = env_sec_mpe['op.program.concentration.area'].search([])
        log.info(f"[secretaria_xyzq @ MPESI] Áreas de Concentração: {len(areas_mpe)}")
        assert len(areas_mpe) == 2, f"Deveria ver 2 áreas do MPESI, viu {len(areas_mpe)}"

        lines_mpe = env_sec_mpe['op.program.research.line'].search([])
        log.info(f"[secretaria_xyzq @ MPESI] Linhas de Pesquisa: {len(lines_mpe)}")
        assert len(lines_mpe) == 4, f"Deveria ver 4 linhas do MPESI, viu {len(lines_mpe)}"

        projects_mpe = env_sec_mpe['capes.research.project'].search([])
        log.info(f"[secretaria_xyzq @ MPESI] Projetos de Pesquisa: {len(projects_mpe)}")
        assert len(projects_mpe) == 2, f"Deveria ver 2 projetos do MPESI, viu {len(projects_mpe)}"

        batches_mpe = env_sec_mpe['op.batch'].search([])
        log.info(f"[secretaria_xyzq @ MPESI] Turmas visíveis: {len(batches_mpe)}")
        assert len(batches_mpe) == 1, f"secretaria_xyzq com MPESI ativo deveria ver 1 turma, viu {len(batches_mpe)}"
        students_mpe = env_sec_mpe['op.student'].search([])
        log.info(f"[secretaria_xyzq @ MPESI] Discentes visíveis: {len(students_mpe)}")
        assert len(students_mpe) == 25, f"secretaria_xyzq com MPESI ativo deveria ver 25 discentes, viu {len(students_mpe)}"

        # 2c. Tentar alternar para programa NÃO autorizado (ex: DFIS) -> Deve lançar AccessError
        try:
            env_sec_multi['res.users'].action_switch_program(prog_map['PPGFA'])
            assert False, "secretaria_xyzq não deveria conseguir alternar para PPGFA!"
        except odoo.exceptions.AccessError:
            log.info("[secretaria_xyzq] Bloqueio contra programa não autorizado validado com sucesso!")

        # 3. Testar Secretaria Setorial Monoprograma (secretaria: apenas PPGCC)
        user_sec_single = env['res.users'].search([('login', '=', 'secretaria')], limit=1)
        assert user_sec_single, "Usuário secretaria não encontrado!"
        env_sec_single = api.Environment(cr, user_sec_single.id, {})

        sec_single_progs = env_sec_single['op.program.capes'].search([])
        sec_single_prog_names = [p.short_name for p in sec_single_progs]
        log.info(f"[secretaria] Programas visíveis: {sec_single_prog_names}")
        assert sec_single_prog_names == ['PPGCC'], f"Esperado apenas PPGCC, obtido: {sec_single_prog_names}"

        sec_single_batches = env_sec_single['op.batch'].search([])
        log.info(f"[secretaria] Turmas visíveis: {len(sec_single_batches)}")
        assert len(sec_single_batches) == 1, f"secretaria deveria ver 1 turma, viu {len(sec_single_batches)}"

        sec_students = env_sec_single['op.student'].search([])
        log.info(f"[secretaria PPGCC] Discentes visíveis: {len(sec_students)}")
        assert len(sec_students) == 20, f"secretaria deveria ver 20 discentes do PPGCC, viu {len(sec_students)}"

        # 4. Testar Coordenador Setorial (coord_mpesi: apenas MPESI)
        user_coord_mpesi = env['res.users'].search([('login', '=', 'coord_mpesi')], limit=1)
        assert user_coord_mpesi, "Usuário coord_mpesi não encontrado!"
        env_coord_mpesi = api.Environment(cr, user_coord_mpesi.id, {})

        coord_mpesi_progs = env_coord_mpesi['op.program.capes'].search([])
        coord_mpesi_names = [p.short_name for p in coord_mpesi_progs]
        log.info(f"[coord_mpesi] Programas visíveis: {coord_mpesi_names}")
        assert coord_mpesi_names == ['MPESI'], f"Esperado apenas MPESI, obtido: {coord_mpesi_names}"

        coord_mpesi_batches = env_coord_mpesi['op.batch'].search([])
        log.info(f"[coord_mpesi] Turmas visíveis: {len(coord_mpesi_batches)}")
        assert len(coord_mpesi_batches) == 1, f"coord_mpesi deveria ver 1 turma, viu {len(coord_mpesi_batches)}"

        # 5. Testar Discentes visíveis para coord_mpesi:
        # Ele vê os 25 discentes do MPESI (como coordenador do programa ativo)
        # + 2 discentes do PPGCC dos quais ele é o Orientador oficial (Daniel Penna e Eduarda Marinho)
        # Totalizando 27 discentes legítimos
        coord_students = env_coord_mpesi['op.student'].search([])
        log.info(f"[coord_mpesi] Discentes visíveis (25 MPESI + 2 orientandos PPGCC): {len(coord_students)}")
        assert len(coord_students) == 27, f"coord_mpesi deveria ver 27 discentes legítimos, viu {len(coord_students)}"

        log.info("✔ TODOS OS TESTES DE ISOLAMENTO EM 'universidade_xyzq' PASSARAM COM SUCESSO!\n")


def test_mptrcs_monoprogram():
    log.info("=== TESTANDO TRANSPARÊNCIA MONOPROGRAMA EM 'mptrcs_ipen_prod' ===")
    odoo.tools.config.parse_config(['-c', CONFIG_PATH, '-d', 'mptrcs_ipen_prod', '--no-http'])
    registry = Registry('mptrcs_ipen_prod')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        programs = env['op.program.capes'].search([])
        log.info(f"Programas no MPTRCS: {[p.name for p in programs]}")
        assert len(programs) == 1, f"MPTRCS deve ter exatamente 1 programa, tem {len(programs)}"

        user_sec = env['res.users'].search([('login', '=', 'secretaria')], limit=1)
        assert user_sec, "Usuário secretaria não encontrado no MPTRCS!"
        env_sec = api.Environment(cr, user_sec.id, {})

        sec_progs = env_sec['op.program.capes'].search([])
        log.info(f"[secretaria MPTRCS] Programas visíveis: {len(sec_progs)}")
        assert len(sec_progs) == 1, f"Secretaria deve ver o único programa, viu {len(sec_progs)}"

        sec_batches = env_sec['op.batch'].search([])
        log.info(f"[secretaria MPTRCS] Turmas visíveis: {len(sec_batches)}")
        assert len(sec_batches) == 4, f"Secretaria deve ver 4 turmas, viu {len(sec_batches)}"

        sec_students = env_sec['op.student'].search([])
        log.info(f"[secretaria MPTRCS] Discentes visíveis: {len(sec_students)}")
        assert len(sec_students) == 60, f"Secretaria deve ver todos os 60 discentes, viu {len(sec_students)}"

        log.info("✔ TESTE MONOPROGRAMA NO 'mptrcs_ipen_prod' PASSOU COM SUCESSO!\n")


if __name__ == '__main__':
    test_xyzq_isolation()
    test_mptrcs_monoprogram()
    log.info("=====================================================================")
    log.info("VALIDAÇÃO CONCLUÍDA COM 100% DE APROVAÇÃO EM AMBOS OS AMBIENTES!")
    log.info("=====================================================================")
