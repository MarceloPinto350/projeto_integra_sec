import axios from 'axios';

export default {
    data () {      
        return {
            aplicacoes: [],
        };
    },
    mounted () {    
        axios.get('/aplicacoes/')
            .then(response => {
                this.aplicacoes = response.data;
            })
            .catch(error => {
                console.error(error);
            });
    },
};
