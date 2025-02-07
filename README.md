# 2024-2B-T10-SI08-G02
# Inteli - Instituto de Tecnologia e Liderança

<img src="./assets/inteli.png" alt="Logo Inteli">

# Integração, Gerenciamento e Análise de Big Data
## Grupo Paulista de Transporte Metropolitano - GPTM

<p align="justify"> &emsp;&emsp; Este MVP apresenta um pipeline de Big Data desenvolvido para centralizar e processar dados operacionais e administrativos da CPTM. O projeto utiliza o processo de ETL (Extract, Transform and Load), no qual os dados foram extraídos, transformados e tratados para garantir sua qualidade e consistência. A partir desses dados processados, foram realizadas análises que resultaram na criação de gráficos exibidos em um front-end. Esses gráficos permitem a extração de insights estratégicos, contribuindo para a otimização das operações e para a tomada de decisões na CPTM. </p>

### 👤 Integrantes:

• [Davi Motta](https://www.linkedin.com/in/davi-motta/) </br>
• [Lucas Galvão](https://www.linkedin.com/in/lucas-galv%C3%A3o/) </br>
• [Marcelo Sitton](https://www.linkedin.com/in/marcelo-sitton-878248271/) </br>
• [Mateus Marçal](https://www.linkedin.com/in/mateus-mar%C3%A7al/) </br>
• [Michel Khafif](https://www.linkedin.com/in/michel-khafif/) </br>
• [Otto Lima](https://www.linkedin.com/in/otto-bernardo-coutinho-lima/) </br>
• [Ricardo Novaes](https://www.linkedin.com/in/ricardo-novaes-24276b271/)

## 📁 Estrutura de Pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: aqui estão os arquivos relacionados a parte gráfica do projeto, as imagens e vídeos que os compõem.

- <b>document</b>: aqui estão os arquivos relacionados aos documentos desenvolvidos durante o projeto, bem como a pasta 'apresentação' na qual se encontram as apresentações realizados ao parceiro durante as sprints.

- <b>src</b>: aqui estão os arquivos de código fonte, histórico de versões e outros arquivos técnicos desenvolvidos durante o projeto.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto - você está aqui agora.

## ⚙️ Requisitos
Para participar deste módulo, você precisará:
- Computador com acesso à internet.
- Software e ferramentas específicos mencionados nas instruções do módulo.

## 🛠️ Instalação

Para instalar este projeto, você deve clonar este repositório para o seu computador e abri-lo em uma IDE de sua preferência, aqui recomenda-se o uso do [Visual Studio Code](https://code.visualstudio.com/download). Além disso, é necessário ter Python instalado em sua máquina.


1. **Inicialização do Ambiente**:
   - Certifique-se de que todas as conexões e configurações estão corretas em `.env` e os arquivos de configuração em `src/dataapp/config/`. Após a verificação, dentro do repositório, abra a pasta 'src' utilizando o seguinte comando:

    ```
        cd . /src
    ```

    Após isso, instale gerenciador de pacotes 'poetry' através do seguinte comando:

        pip install poetry

   

    Posteriormente inicia-se o o poetry  os seguintes comandos:

    ```
      poetry install
    ```
    
    ```
        poetry shell
    ```

    Para assegurar-se que todas as dependências do projeto estejam devidamente atualizadas, neste ponto faz-se essencial abrir o Docker Desktop e executar o comando `docker-compose up`.

2. **Execução do ETL**:
   - O pipeline ETL é automatizado com Prefect. As tarefas são definidas e agendadas para execução através do Prefect Cloud, monitorando métricas de execução.

3. **Iniciar a API**:
   - Execute o seguinte comando para iniciar a API Flask:

```
 python -m dataapp.api  
```

4. **Iniciar o Frontend**:
   - Para iniciar o frontend Streamlit, rode:
```
 streamlit run ./dataapp/fronted/app.py 
```

5. **Monitoramento e Logs**:
   - O monitoramento da aplicação pode ser acompanhado através das configurações definidas em `observability.py`, com logs e métricas sendo enviados para o Prefect Cloud.




## 👨‍🏫 Conteúdo do Módulo

- Sprint 1:
   - Entendimento de Negócio;
   - Entendimento do Usuário
   - Análise Exploratória dos Dados.
- Sprint 2:
   - Prototipação em Baixa fidelidade da visualização de dados do projeto, com foco na experiência do usuário;
   - Estrutura de Ingestão de Dados.
- Sprint 3:
   - Cubo de Dados Automatizado;
   - Documentação de análise de impacto ético.
- Sprint 4:
   - Criação de Infográfico e relatório de análise de eficácia do mesmo com sugestão de melhorias;
   -DataAPP - Primeira Versão;
   - Análise financeira do projeto e Plano de comunicação.
- Sprint 5:
   - Documentação completa da solução;
   - DataAPP - versão final refinada;  
   - Avaliação final e encerramento do módulo.


##  Histórico de Lançamentos

- 0.1.0 - 25/10/2024 </br>
  -  Primeira entrega: Entendimento de negócio, Análise Exploratória dos Dados e Entendimento de UX

- 0.2.0 - 08/11/2024 </br>
  - Segunda entrega: Wireframes de Baixa Fidelidade, Ingestão de Dados

- 22/11/2024 </br>
  - Terceira entrega: Documentação de análise de impacto ético, Cubo de Dados Automatizado

- 0.4.0 - 06/12/2024 </br>
  - Quarta entrega: DataAPP - Primeira Versão, Criação de Infográfico, Análise Financeira e Plano de Comunicação 

- 1.0.0 - 17/12/2024 </br>
  - Quinta entrega: Versão Final do Data App e Documentação Completa

## 📋 Licença

[Integração, Gerenciamento e Análise de Big Data]() por [Inteli](https://github.com/InteliProjects), [Grupo 2](https://github.com/Inteli-College/2024-2B-T10-SI08-G02): [Davi Motta](https://www.linkedin.com/in/davi-motta/), [Lucas Galvão](https://www.linkedin.com/in/lucas-galv%C3%A3o/), [Marcelo Sitton](https://www.linkedin.com/in/marcelo-sitton-878248271/),  [Mateus Marçal](https://www.linkedin.com/in/mateus-mar%C3%A7al/), [Michel Khafif](https://www.linkedin.com/in/michel-khafif/), [Otto Lima](https://www.linkedin.com/in/otto-bernardo-coutinho-lima/) e [Ricardo Novaes](https://www.linkedin.com/in/ricardo-novaes-24276b271/) está licenciado sob [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
