<template>
    <div class="aplicacao-cadastrar">
        <h2>Cadastrar aplicação</h2>
        <form @submit.prevent="cadastrarAplicacao">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" v-model="aplicacao.nome" required>
            </div>
            <div class="form-group">
                <label for="sigla">Sigla:</label>
                <input type="text" id="sigla" v-model="aplicacao.sigla" required>
            </div>    
            <div class="form-group">
                <label for="descricao">Descrição:</label>
                <input type="text" id="descricao" v-model="aplicacao.descricao" required>
            </div>
            <div class="form-group">
                <label for="categoria">Categoria:</label>
                <select id="categoria" v-model="aplicacao.categoria" required>
                    <option value="ADMINISTRATIVA">Administrativa</option>
                    <option value="TI">Tecnologia da Informação</option>
                    <option value="JUDICIAL">Judicial</option>
                <input type="text" id="categoria" v-model="aplicacao.categoria" required>
            </div>
            <div class="form-group">
                <label for="url_fonte">URL do código fonte:</label>
                <input type="url" id="url_fonte" v-model="aplicacao.url_fonte" required>   
            </div>
            <div class="form-group">    
                <label for="area_reponsavel">Área responsável:</label>  
                <select id="areanegocial.id" v-model="areanegocial.nome" required>
            </div>
            <div class="form-group">    
                <label for="tipo">Tipo aplicação:</label>
                <select id="tipoaplicacao.id" v-model="tipoaplicacao.nome" required>
            </div>
            <div class="form-group">
                <label for="data_descontinuacao">Data de descontinuação:</label>
                <input type="date" id="data_descontinuacao" v-model="aplicacao.data_descontinuacao">
            </div>
            <div class="form-group">
                <label for="arquitetura">Arquitetura:</label>
                <select id="arquitetura" v-model="aplicacao.arquitetura" required>
                    <option value="WEB">Web</option>
                    <option value="CLIENTE/SERVIDOR">Cliente/Servidor</option>
                    <option value="MAINFRAME">Mainframe</option>
                </select>
            </div>
            <div class="form-group">
                <label for="hospedagem">Hospedagem:</label>
                <select id="hospedagem" v-model="aplicacao.hospedagem" required>
                    <option value="LOCAL">Local</option>
                    <option value="CLOUD">Cloud</option>
                    <option value="HÍBRIDO">Híbrido</option>
                    <option value="EXTERNO">Externo</option>
                </select>
            </div>
            <select v-model="selected">
                <option v-for="aplicacao in aplicacoes" :key="aplicacao.id">
                    {{ aplicacao.nome }}
                </option>
            </select>
            <div class="form-group">
                <label for="aplicacao_pai">Aplicação pai:</label>
                selected: {{ selected }}
            </div> 
            <div class="form-group">
                <label for="usuario_servico">Usuário de serviço:</label>
                <input type="text" id="usuario_servico" v-model="aplicacao.usuario_servico" required>   
            </div>
            <div class="form-group">
                <label for="senha_servico">Senha de serviço:</label>
                <input type="password" id="senha_servico" v-model="aplicacao.senha_servico" required>   
            </div>
            <div class="form-group">
                <label for="token_acesso">Token de acesso:</label>
                <input type="text" id="token_acesso" v-model="aplicacao.token_acesso" required>
            </div>
            <div class="form-group">
                <label for="url_acesso">URL de acesso:</label>
                <input type="url" id="url_acesso" v-model="aplicacao.url_acesso" required>
            </div>
            <button type="submit">Cadastrar</button>
        </form>
    </div>
</template>