<template>
    <div class="aplicacao-listar">
        <h2>Lista de aplicações</h2>
        <ul>
            <li v-for="aplicacao in aplicacoes" :key="aplicacao.id">
                {{ nome }} - {{ descricao }} - {{ descricao }} - {{ categoria}}    
                <a :href="aplicacao.url_acesso">Acessar</a>
                <a :href="aplicacao.url_fonte">Código fonte</a>
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data () {      
            return {
                aplicacoes: [],
            };
        },
        mounted () {    
            axios.get('/api/aplicacoes/')
                .then(response => {
                    this.aplicacoes = response.data;
                })
                .catch(error => {
                    console.error(error);
                });
        },
    };
</script>