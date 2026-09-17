#!/usr/bin/env python3
"""
Renderizador de Documentação Técnica e Manuais em HTML
Converte todos os arquivos .md em docs/ e o README.md na raiz em arquivos HTML
com estilização moderna, tipografia refinada, suporte a tabelas e índice navegável.
"""
import os
import subprocess
import glob
from pathlib import Path

CSS_STYLES = """
:root {
    --primary: #1e3a8a;
    --primary-light: #3b82f6;
    --secondary: #0f172a;
    --bg: #ffffff;
    --bg-alt: #f8fafc;
    --text: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --code-bg: #f1f5f9;
    --accent-bg: #eff6ff;
    --accent-border: #bfdbfe;
    --success-bg: #ecfdf5;
    --success-border: #a7f3d0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--text);
    background-color: var(--bg);
    line-height: 1.65;
    max-width: 960px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--secondary);
    font-weight: 700;
    margin-top: 2rem;
    margin-bottom: 0.75rem;
    line-height: 1.25;
}

h1 {
    font-size: 2.1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
    color: var(--primary);
}

h2 {
    font-size: 1.5rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--border);
}

h3 {
    font-size: 1.25rem;
}

p {
    margin-bottom: 1.2rem;
}

a {
    color: var(--primary-light);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.92rem;
    background: var(--bg);
}

th, td {
    padding: 0.65rem 0.85rem;
    border: 1px solid var(--border);
    text-align: left;
}

th {
    background-color: var(--bg-alt);
    font-weight: 600;
    color: var(--secondary);
}

tr:nth-child(even) td {
    background-color: #fafbfc;
}

code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.88em;
    background-color: var(--code-bg);
    padding: 0.15rem 0.35rem;
    border-radius: 4px;
    color: #0f172a;
}

pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.88rem;
    line-height: 1.45;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
}

blockquote {
    margin: 1.5rem 0;
    padding: 0.8rem 1.2rem;
    border-left: 4px solid var(--primary-light);
    background-color: var(--accent-bg);
    color: #1e3a8a;
    border-radius: 0 6px 6px 0;
}

blockquote p:last-child {
    margin-bottom: 0;
}

ul, ol {
    padding-left: 1.5rem;
    margin-bottom: 1.2rem;
}

li {
    margin-bottom: 0.35rem;
}

hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.5rem 0;
}

#TOC {
    background: var(--bg-alt);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 2.5rem;
}

#TOC ul {
    margin-bottom: 0;
    padding-left: 1.2rem;
}

#TOC > ul {
    padding-left: 0;
    list-style: none;
}

.nav-bar {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
}

.nav-bar a {
    margin-right: 1rem;
    font-weight: 500;
}
"""

def get_title_from_md(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return os.path.basename(file_path)

def render_markdown(src_path, dest_path, title=None):
    if not title:
        title = get_title_from_md(src_path)
    
    css_file = "/tmp/doc_style.css"
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(CSS_STYLES)
        
    cmd = [
        "pandoc",
        str(src_path),
        "-s",
        "-o", str(dest_path),
        "--toc",
        f"--metadata=title:{title}",
        f"--css={css_file}",
        "--embed-resources",
        "--standalone"
    ]
    
    subprocess.run(cmd, check=True)
    print(f"[OK] Gerado: {dest_path}")

def generate_index_html(docs_dir, sections):
    index_path = Path(docs_dir) / "index.html"
    
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenEduCat CAPES - Portal da Documentação Técnica</title>
    <style>
""" + CSS_STYLES + """
    .doc-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    .doc-card {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.25rem;
        background: var(--bg);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .doc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: var(--accent-border);
    }
    .doc-card h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.15rem;
    }
    .doc-card ul {
        list-style: none;
        padding-left: 0;
        margin-bottom: 0;
    }
    .doc-card li {
        margin-bottom: 0.4rem;
        font-size: 0.95rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 4px;
        background: var(--accent-bg);
        color: var(--primary);
        margin-bottom: 0.75rem;
    }
    .badge-highlight {
        background: var(--success-bg);
        color: #065f46;
        border: 1px solid var(--success-border);
    }
    </style>
</head>
<body>
    <div class="nav-bar">
        <a href="../README.html">← Voltar ao README Principal</a>
        <a href="documentacao_executiva_capes.html">Documentação Executiva (Quarto)</a>
    </div>

    <h1>OpenEduCat CAPES — Portal de Documentação & Manuais</h1>
    <p>Guia central unificado para administradores, secretarias acadêmicas, coordenadores de pós-graduação, docentes e discentes.</p>
"""

    for sec_title, sec_badge, files in sections:
        html += f"""
    <h2>{sec_title}</h2>
    <div class="doc-grid">
"""
        for title, rel_html_path, desc in files:
            html += f"""
        <div class="doc-card">
            <span class="badge { 'badge-highlight' if 'Manual' in sec_title or 'Implantação' in sec_title else '' }">{sec_badge}</span>
            <h3><a href="{rel_html_path}">{title}</a></h3>
            <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 0;">{desc}</p>
        </div>
"""
        html += "    </div>\n"

    html += """
    <hr>
    <footer style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 2rem;">
        OpenEduCat Brasil Stricto Sensu (CAPES / DAV / Sucupira) &bull; Odoo 19.0 &bull; IPEN / CNEN / USP
    </footer>
</body>
</html>
"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Portal da Documentação gerado em: {index_path}")

def main():
    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = repo_root / "docs"

    # 1. Renderizar README.md
    readme_md = repo_root / "README.md"
    readme_html = repo_root / "README.html"
    render_markdown(readme_md, readme_html, "OpenEduCat CAPES - Especificação Técnica do Sistema")

    # 2. Renderizar todos os .md em docs/
    all_md_files = list(docs_dir.rglob("*.md"))
    for md_file in all_md_files:
        html_file = md_file.with_suffix(".html")
        render_markdown(md_file, html_file)

    # 3. Categorizar para o index.html
    sections = [
        (
            "1. Implantação e Manuais Operacionais do Cotidiano",
            "Operação",
            [
                ("Inicialização de Banco Zerado e Migração", "10_implantacao_e_migracao/01_inicializacao_banco_zerado_e_migracao.html", "Roteiro completo de bootstrap com banco vazio, provisionamento e carga CSV."),
                ("Manual de Operação: Secretaria Acadêmica", "11_manuais_operacionais/01_manual_secretaria.html", "Matrículas, aproveitamento intra/extra IES, alunos especiais e livro-razão."),
                ("Manual de Operação: Coordenação de Programa (CPG)", "11_manuais_operacionais/02_manual_coordenacao.html", "Gestão de vagas, relatórios Sucupira, deliberações de CPG e homologação."),
                ("Manual de Operação: Professores & Orientadores", "11_manuais_operacionais/03_manual_professores.html", "Lançamento de notas, gestão de orientandos, aprovação de PTTs e bancas."),
                ("Manual de Operação: Alunos & Portal do Discente", "11_manuais_operacionais/04_manual_alunos.html", "Requerimentos online, consulta de integralização de créditos e depósito de dissertação."),
            ]
        ),
        (
            "2. Arquitetura Sistêmica & Governança Curricular",
            "Arquitetura",
            [
                ("Visão Geral e Governança Regimental (GoPG)", "01_arquitetura_sistemica/01_visao_geral_e_gopg.html", "Princípios de DDD, motor cronológico e governança de programas."),
                ("Topologia do Monorepo", "01_arquitetura_sistemica/02_topologia_do_monorepo.html", "Estrutura dos 8 submódulos e matriz de dependências."),
                ("Motor de Versionamento de Regimentos", "02_governanca_regimental_e_creditos/01_motor_de_versionamento.html", "Modelagem dinâmica de regimentos e parametrização."),
                ("Ato Jurídico Perfeito e Hibridismo", "02_governanca_regimental_e_creditos/02_ato_juridico_perfeito_e_hibridismo.html", "Preservação histórica de créditos e regras de transição."),
                ("Livro-Razão Acadêmico e Integralização", "02_governanca_regimental_e_creditos/03_livro_razao_e_integralizacao.html", "Tabelas append-only e motor de cálculo de créditos."),
            ]
        ),
        (
            "3. Produtos Técnico-Tecnológicos (PTT) & Titulação",
            "Regulatório CAPES",
            [
                ("Taxonomia PTT, Eixos e Tipos", "05_produtos_tecnico_tecnologicos_ptt/01_taxonomia_eixos_e_tipos.html", "Classificação completa dos 14 tipos de produtos técnicos da Portaria CAPES."),
                ("Qualis Tecnológico e Workflow de Validação", "05_produtos_tecnico_tecnologicos_ptt/02_qualis_tecnologico_e_workflow.html", "Fluxo de chancela de produtos e homologação pela CPG."),
                ("Cálculo de Estratos PTT e BI", "05_produtos_tecnico_tecnologicos_ptt/03_calculo_de_estratos_e_bi.html", "Motor de pontuação de impacto e inovação tecnológica."),
                ("Rito Bipartido e Bancas Examinadoras", "06_titulacao_e_conformidade_documental/01_rito_bipartido_e_bancas.html", "Qualificação, defesa final e composição de comissões."),
                ("Histórico Escolar Consolidado e Diploma Digital", "06_titulacao_e_conformidade_documental/02_historico_escolar_consolidado.html", "Emissão documental segundo normas MEC e carimbo XML."),
            ]
        ),
        (
            "4. Validações Específicas do Programa MPTRCS (IPEN / CNEN)",
            "Caso Real MPTRCS",
            [
                ("MP01: Estrutura Curricular e Créditos do MPTRCS", "09_validacoes_mptrcs/mp01_detalhamento_validacao_mptrcs.html", "Regras específicas de 100 créditos (24 cursados + 76 tese)."),
                ("MP02 a MP10: Validações Detalhadas do MPTRCS", "09_validacoes_mptrcs/mp02_detalhamento_validacao_mptrcs.html", "Aproveitamento de créditos, proficiência, bancas e conformidade."),
            ]
        )
    ]

    generate_index_html(docs_dir, sections)
    print("\n✓ Todos os arquivos HTML foram gerados com sucesso!")

if __name__ == "__main__":
    main()
