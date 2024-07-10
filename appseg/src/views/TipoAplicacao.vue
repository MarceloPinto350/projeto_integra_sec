<template>

    <div class="tipo-aplicacao">
        <h1>Tipos de Aplicação</h1>
        <p>Esta é uma aplicação Vue.js simples que demonstra como usar o Vue Router para criar uma aplicação de várias páginas.</p>
        <div v-for="tipo in APIData" :key="tipo.id">
            <router-link :to="{ name: 'TipoAplicacaoDet', params: { id: tipo.id, nome: tipo.nome, descricao: tipo.descricao }}">
                <h2>{{ tipo.nome }}</h2>
            </router-link>
            {{ tipo.descricao }}
        </div>
    </div>
</template>

<script>
    import { getAPI } from '../axios-api';

    export default {
        name: 'TipoAplicacao',
        data() {
            return {
                APIData: [],
            };
        },
        created() {
            try {
                const response = getAPI.get('/tiposaplicacao/');
                console.log('Dados recuperados da API');
                this.APIData = response.data;
            } catch (error) {
                console.log(error);
            }
        },
    };  
</script>