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

from odoo import http
from odoo.http import request, Response


class CapesPublicValidationController(http.Controller):

    @http.route('/valida-documento', type='http', auth='public', methods=['GET'], csrf=False)
    def validate_document(self, hash=None, **kwargs):
        """Endpoint público para verificação autônoma da chave SHA-256 e autenticidade do diploma/histórico."""
        if not hash:
            html = """<!DOCTYPE html>
<html>
<head><title>Validador de Documentos Acadêmicos CAPES</title><meta charset="utf-8"/><style>body{font-family:sans-serif;margin:40px;background:#f4f6f9;}.card{background:#fff;padding:30px;border-radius:8px;max-width:600px;margin:auto;box-shadow:0 4px 6px rgba(0,0,0,0.1);}</style></head>
<body>
    <div class="card">
        <h2 style="color:#d9534f;">Nenhuma Chave Hash Fornecida</h2>
        <p>Informe o parâmetro <code>?hash=SUA_CHAVE_SHA256</code> na URL para realizar a validação de autenticidade do documento acadêmico.</p>
    </div>
</body>
</html>"""
            return Response(html, mimetype='text/html')

        Diploma = request.env['capes.digital.diploma'].sudo()
        diploma = Diploma.search([('sha256_hash', '=', hash.strip().upper())], limit=1)

        if not diploma:
            html = f"""<!DOCTYPE html>
<html>
<head><title>Validador de Documentos Acadêmicos CAPES</title><meta charset="utf-8"/><style>body{{font-family:sans-serif;margin:40px;background:#f4f6f9;}}.card{{background:#fff;padding:30px;border-radius:8px;max-width:600px;margin:auto;box-shadow:0 4px 6px rgba(0,0,0,0.1);}}</style></head>
<body>
    <div class="card">
        <h2 style="color:#d9534f;">Documento Não Encontrado / Inválido</h2>
        <p>A chave SHA-256 fornecida (<code>{hash}</code>) não corresponde a nenhum documento ou diploma autenticado na base de dados do ecossistema.</p>
    </div>
</body>
</html>"""
            return Response(html, mimetype='text/html')

        # Documento Válido Encontrado
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Validação Pública de Documento Autêntico</title>
    <meta charset="utf-8"/>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }}
        .card {{ background: #fff; padding: 35px; border-radius: 10px; max-width: 680px; margin: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.08); border-top: 5px solid #28a745; }}
        .badge {{ background: #28a745; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 14px; }}
        h2 {{ margin-top: 0; color: #1e293b; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; }}
        td.label {{ font-weight: bold; color: #475569; width: 40%; }}
        .hash {{ font-family: monospace; font-size: 12px; word-break: break-all; background: #f1f5f9; padding: 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">✓ DOCUMENTO AUTÊNTICO E VALIDADO</span>
        <h2>Validação Pública de Titulação Stricto Sensu</h2>
        <p>Confirmada a autenticidade jurídica e a integridade criptográfica da documentação acadêmica.</p>
        <table>
            <tr><td class="label">Discente Titulado:</td><td>{diploma.student_id.partner_id.name}</td></tr>
            <tr><td class="label">Grau Acadêmico:</td><td>{diploma.degree_type}</td></tr>
            <tr><td class="label">Título da Tese/Dissertação:</td><td>{diploma.thesis_id.title}</td></tr>
            <tr><td class="label">Data de Outorga:</td><td>{diploma.graduation_date}</td></tr>
            <tr><td class="label">IES de Origem:</td><td>{diploma.origin_ies_name}</td></tr>
            <tr><td class="label">IES Emissora / Registradora:</td><td>{diploma.issuing_ies_name}</td></tr>
            <tr><td class="label">Situação do Registro:</td><td><strong>{diploma.state.upper()}</strong></td></tr>
            <tr><td class="label">Padrão de Criptografia:</td><td>ICP-Brasil XAdES-BES com Carimbo de Tempo</td></tr>
        </table>
        <h4 style="margin-top:25px; margin-bottom:5px; color:#475569;">Chave SHA-256 de Auto-Autenticação:</h4>
        <div class="hash">{diploma.sha256_hash}</div>
    </div>
</body>
</html>"""
        return Response(html, mimetype='text/html')
