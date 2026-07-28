# Documento 01: Interoperabilidade e APIs RESTful (Fonte Prata)

## 1. O Paradigma da Interoperabilidade Ativa (RICA|PG)

Com o advento do GoPG e da Rede de Integração da Comunidade Acadêmica da Pós-Graduação (RICA|PG), o OpenEduCat assume o papel de **Fonte Prata** de forma ativa e automatizada.

O submódulo `l10n_br_openeducat_capes_integration` expõe controladores RESTful no Odoo sob a rota padronizada `/api/capes/v1/`, entregando payloads JSON tipados para varredura passiva pelos robôs da CAPES.

## 2. Padronização dos Endpoints da Fonte Prata

As rotas expostas pela Fonte Prata compreendem:

* `GET /api/capes/v1/students`: Devolve o cadastro de discentes ativos e titulados, incluindo PIDs (CPF, ORCiD, Lattes), etnia, gênero, data de admissão, status, orientador, status de proficiência e chave do regimento (`curriculum_version_id`).
* `GET /api/capes/v1/faculty`: Devolve o corpo docente, PIDs, regime de trabalho e a timeline de credenciamento derivada do livro-razão `op.faculty.category.ledger`.
* `GET /api/capes/v1/curriculums`: Expõe a matriz de disciplinas ativas, ementas, carga horária/créditos, regulamentos e modalidade de ensino.
* `GET /api/capes/v1/projects_and_ptts`: Exporta os projetos de pesquisa cadastrados, relacionando-os com as dissertações defendidas e os Produtos Técnico-Tecnológicos (PTTs) com seus respectivos estratos Qualis calculados.

## 3. Estrutura do Payload JSON (Exemplo Discentes)

```json
{
  "ies_emec_code": "12345",
  "program_snpg_code": "33002010123P4",
  "data": [
    {
      "internal_id": "OP-STU-2026-001",
      "fiscal_name": "João da Silva",
      "pids": {
        "cpf": "12345678909",
        "orcid": "0000-0002-1825-0097",
        "lattes_url": "http://lattes.cnpq.br/1234567890123456"
      },
      "admission_date": "2024-02-15",
      "curriculum_version": "Regimento IPEN 2024",
      "status": "Matriculado",
      "english_proficiency": "Approved",
      "advisor_orcid": "0000-0001-9876-5432",
      "research_line": "Medicina Nuclear e Dosimetria"
    }
  ],
  "meta": {
    "timestamp": "2026-07-27T14:30:00Z",
    "total_records": 1
  }
}

```

## 4. Segurança, Autenticação e LGPD

* **Autenticação (OAuth 2.0 / mTLS):** O acesso às rotas da Fonte Prata é protegido via *Client Credentials* com tokens de curta duração e Mutual TLS.
* **Privacy by Design:** Dados estritamente privados (financeiro, telefones pessoais, prontuários de afastamentos médicos sem CID público) são removidos do serializador JSON.
