import networkx as nx
import matplotlib.pyplot as plt

#Cria um objeto grafo
G = nx.Graph()


# tipos de vértices
# 1) Aplicação
# 2) Ferramenta de varredura
# 3) Banco de dados
# 4) Servidor
# 5) Rede
# 6) Serviço
# 7) Ativo de infraestrutura # NÃO INCLUIR ESSE TÓPICO


def adicionar_aresta(vertice1, vertice2):
    G.add_edge(vertice1, vertice2)    


def adicionar_vertice(vertice, tipo):
    # buscar os vértices do grafo através dos cadastros de aplicações
    G.add_node(vertice, tipo=tipo)
    
def gera_grafo(relacoes):
    """Método que monta o json para o grafo cujo os dados são provenientes do banco de dados de relacionamentos
    
    Deve restornar um json no seguinte formato:
    dados = [
        {"source": "aplicacao1", "target": "ativo1"},
        {"source": "aplicacao1", "target": "ativo2"},
        ...
    ]
    """
    dados = []
    if relacoes:
        for relacao in relacoes:
            dados.append({"source": relacao[0], "target": relacao[1]})
    
    return (dados)


def montar_grafo_manual():
    print ("Adicionando vértices")
    adicionar_vertice('DVWA','Aplicação')
    adicionar_vertice('SonarQube','Teste Segurança') 
    adicionar_vertice('PostgreSQL-Geral','Banco de Dados') 
    adicionar_vertice('Containernet','Servidor')
    adicionar_vertice('Rede Containernet', 'Rede')
    adicionar_vertice('Owasp-ZAP','Teste Segurança')
    adicionar_vertice('Owasp-DC','Teste Segurança') 
    adicionar_vertice('AppSeg','Aplicação') 
    adicionar_vertice('MySQL-Geral','Banco de Dados')  
    adicionar_vertice('Oracle-Geral','Banco de Dados') 
    adicionar_vertice('PROAD','Aplicação')  
    adicionar_vertice('Assunto-Proad','Módulo')  
    adicionar_vertice('Consulta-Proad','Módulo') 
    adicionar_vertice('SonarQube-CLI','Serviço')
    adicionar_vertice('PJe','Aplicação')  
    adicionar_vertice('PJe-Consulta','Módulo')
    adicionar_vertice('PJe-Segurança','Módulo')
    adicionar_vertice('AUD','Satélite') 
    adicionar_vertice('PJe-KZ','Módulo')
    adicionar_vertice('PJe-Calc','Satélite') 
    adicionar_vertice('PJe-Integracao','Satélite') 
    print(f'Vértices adicionados: {G.nodes}')
    print('-----------------------')

    print("Adicionando as arestas")
    adicionar_aresta('DVWA', 'SonarQube') # verifica/é verificado
    adicionar_aresta('DVWA', 'MySQL-Geral') # utiliza/é utilizado
    adicionar_aresta('DVWA', 'AppSeg') # inspeciona/é inspecionado
    adicionar_aresta('AppSeg', 'SonarQube') # conecta/é conectado
    adicionar_aresta('AppSeg', 'SonarQube-CLI') # conecta/é conectado
    adicionar_aresta('AppSeg', 'Owas-DC') # conecta/é conectado
    adicionar_aresta('AppSeg', 'Owasp-ZAP') # conecta/é conectado
    adicionar_aresta('DVWA', 'Containernet') # hospeda/é hospedado
    adicionar_aresta('Containernet', 'Rede Containernet') #integra/é integrado
    adicionar_aresta('SonarQube', 'Containernet') # hospeda/é hospedado
    adicionar_aresta('SonarQube-CLI', 'Containernet') # hospeda/é hospedado
    adicionar_aresta('Owasp-ZAP', 'Containernet') # hospeda/é hospedado
    adicionar_aresta('Owasp-DC', 'Containernet') # hospeda/é hospedado
    print(f'Arestas adicionadas: {G.edges}')
    print('-----------------------')
    print(f"Resumo do grafo... Total de Vértices: {G.number_of_nodes()}; Total de Arestas: {G.number_of_edges()}")
    print()
    #teste de visualização do grafo
    print("Visualizando o grafo")
    G = nx.petersen_graph()
    #plt.subplot()
    nx.draw(G)
    #plt.subplot()
    nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    #plt.plot().savefig('/tmp/grafo.png')
    plt.savefig('/tmp/grafo.png')
    plt.show()
    print('-----------------------')