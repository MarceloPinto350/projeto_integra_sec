<template>
    <div>
        <b-container>
            <h1>Tipos de Aplicação</h1>
            <p>Estes são os tipos de aplicação cadastrados.</p>
            <b-table striped hover :items="APIData" :fields="fields">
                <template v-slot:cell(actions)="data">
                    <b-button size="sm" @click="editTipoAplicacao(data.item.id)">Editar</b-button>
                    <b-button size="sm" @click="deleteTipoAplicacao(data.item.id)">Excluir</b-button>
                </template>
            </b-table>
        </b-container>
    </div>
</template>

<script>
    import { getAPI } from '../axios-api';

    export default {
        name: 'TipoAplicacao',
        data() {
            return {
                APIData: [],
            }
        },
        created() {
            try {
                const response = getAPI.get('/tiposaplicacao/',);
                console.log('Dados recuperados da API');
                this.APIData = response.data;
            } catch (error) {
                console.log(error);
            }
        },
    };  
</script>