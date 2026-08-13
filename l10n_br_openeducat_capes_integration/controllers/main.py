###############################################################################
#
#    CINAS Research Group
#    Copyright (C) 2026-TODAY CINAS Research Group(<https://cinas.ipen.br>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import json
from datetime import datetime
from odoo import http, fields
from odoo.http import request, Response


class CapesIntegrationController(http.Controller):

    def _json_response(self, data, status=200):
        """Retorna uma resposta HTTP JSON padronizada."""
        return Response(
            json.dumps(data, default=str),
            status=status,
            mimetype='application/json'
        )

    @http.route('/api/capes/v1/students', type='http', auth='public', methods=['GET'], csrf=False)
    def get_students(self, **kwargs):
        """Endpoint Fonte Prata: Consulta automatizada de discentes (Privacy by Design)."""
        Student = request.env['op.student'].sudo()
        domain = []

        program_id = kwargs.get('program_id')
        if program_id:
            domain.append(('program_id', '=', int(program_id)))

        students = Student.search(domain)
        student_data = []

        company = request.env.company

        for s in students:
            # Privacy by Design: Exclusão de telefones privados, endereços residenciais e dados financeiros
            student_data.append({
                'internal_id': s.code or f'STU-{s.id}',
                'fiscal_name': s.partner_id.name,
                'pids': {
                    'cpf': s.partner_id.cpf or '',
                    'orcid': s.partner_id.orcid or '',
                    'lattes_url': s.partner_id.lattes_url or '',
                },
                'admission_date': str(s.admission_date) if s.admission_date else '',
                'curriculum_version': s.curriculum_version_id.name if s.curriculum_version_id else '',
                'status': s.capes_status,
                'category': s.category,
                'english_proficiency': s.english_proficiency_status,
                'advisor_orcid': s.main_advisor_id.partner_id.orcid if s.main_advisor_id and s.main_advisor_id.partner_id else '',
                'research_line': s.research_line_id.name if s.research_line_id else '',
            })

        payload = {
            'ies_emec_code': company.emec_code or '',
            'ies_cnpj': company.cnpj or '',
            'data': student_data,
            'meta': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'total_records': len(student_data)
            }
        }
        return self._json_response(payload)

    @http.route('/api/capes/v1/faculty', type='http', auth='public', methods=['GET'], csrf=False)
    def get_faculty(self, **kwargs):
        """Endpoint Fonte Prata: Consulta automatizada de docentes e livros-razão de categoria."""
        Faculty = request.env['op.faculty'].sudo()
        faculties = Faculty.search([])
        faculty_data = []

        company = request.env.company

        for f in faculties:
            # Mapeia histórico do livro-razão de categorias
            ledger_data = []
            for ledger in f.category_ledger_ids:
                ledger_data.append({
                    'category': ledger.category,
                    'start_date': str(ledger.start_date) if ledger.start_date else '',
                    'end_date': str(ledger.end_date) if ledger.end_date else '',
                    'validity': ledger.validity_status
                })

            faculty_data.append({
                'internal_id': f.code or f'FAC-{f.id}',
                'name': f.partner_id.name,
                'pids': {
                    'cpf': f.partner_id.cpf or '',
                    'orcid': f.partner_id.orcid or '',
                    'lattes_url': f.partner_id.lattes_url or '',
                    'scopus_id': f.partner_id.scopus_id or '',
                },
                'work_regime': f.work_regime_gopg,
                'weekly_workload': f.weekly_workload,
                'title_level': f.title_level,
                'category_history': ledger_data
            })

        payload = {
            'ies_emec_code': company.emec_code or '',
            'data': faculty_data,
            'meta': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'total_records': len(faculty_data)
            }
        }
        return self._json_response(payload)

    @http.route('/api/capes/v1/curriculums', type='http', auth='public', methods=['GET'], csrf=False)
    def get_curriculums(self, **kwargs):
        """Endpoint Fonte Prata: Consulta de estruturas curriculares e regras regimentais."""
        Version = request.env['op.curriculum.version'].sudo()
        versions = Version.search([])
        version_data = []

        for v in versions:
            subject_rules = []
            for sr in v.subject_rule_ids:
                subject_rules.append({
                    'subject_name': sr.subject_id.name if sr.subject_id else '',
                    'subject_code': sr.subject_id.code if sr.subject_id else '',
                    'rule_type': sr.rule_type,
                    'area_name': sr.area_id.name if sr.area_id else '',
                    'credits': sr.credits
                })

            version_data.append({
                'version_name': v.name,
                'program_name': v.program_id.name if v.program_id else '',
                'snpg_code': v.program_id.snpg_code if v.program_id else '',
                'min_credits': v.min_credits,
                'min_months': v.min_months,
                'max_months': v.max_months,
                'proficiency_stage': v.proficiency_stage,
                'ptt_validation_mode': v.ptt_validation_mode,
                'teaching_internship_mode': v.teaching_internship_mode,
                'subject_rules': subject_rules
            })

        payload = {
            'data': version_data,
            'meta': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'total_records': len(version_data)
            }
        }
        return self._json_response(payload)

    @http.route('/api/capes/v1/projects_and_ptts', type='http', auth='public', methods=['GET'], csrf=False)
    def get_projects_and_ptts(self, **kwargs):
        """Endpoint Fonte Prata: Exportação de projetos de pesquisa e Produtos Técnico-Tecnológicos (PTTs)."""
        Project = request.env['capes.research.project'].sudo()
        Ptt = request.env['capes.ptt.product'].sudo()

        projects = Project.search([])
        ptts = Ptt.search([])

        project_data = []
        for p in projects:
            project_data.append({
                'project_name': p.name,
                'project_type': p.project_type,
                'research_nature': p.research_nature,
                'is_cooperation': p.is_cooperation,
                'foreign_ies': p.foreign_ies or '',
                'funding_agency': p.funding_agency or '',
                'coordinator_orcid': p.coordinator_id.partner_id.orcid if p.coordinator_id and p.coordinator_id.partner_id else '',
                'status': p.status
            })

        ptt_data = []
        for ptt in ptts:
            ptt_data.append({
                'title': ptt.title,
                'typology_code': ptt.type_id.code if ptt.type_id else '',
                'axis_code': ptt.axis_id.code if ptt.axis_id else '',
                'student_orcid': ptt.student_id.partner_id.orcid if ptt.student_id and ptt.student_id.partner_id else '',
                'trl_level': ptt.trl_level,
                'is_adherent': ptt.is_adherent,
                'final_stratum': ptt.final_stratum,
                'repository_url': ptt.repository_url or '',
                'state': ptt.state
            })

        payload = {
            'data': {
                'research_projects': project_data,
                'ptt_products': ptt_data
            },
            'meta': {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'total_projects': len(project_data),
                'total_ptts': len(ptt_data)
            }
        }
        return self._json_response(payload)
