<script>
  //import AboutView  from './views/AboutView.vue';
  //import HomeView   from './views/HomeView.vue';  
  //import TipoAplicacao from './views/TipoAplicacao.vue';

  import { ref, computed } from 'vue';
  //import { useDateTime } from '@/composables/useDateTime';
  //import { getCurrentUser } from '@/services/user';
  //import { useRouter } from 'vue-router';
  
  export default {
  //  setup() {
  //    const router = useRouter();
  //    const user = ref(null);
  //    const currentDate = computed(() => useDateTime());
  //    const isLoggedIn = computed(() => user.value !== null);

  //    getCurrentUser().then((userData) => {
  //      user.value = userData.name;
  //    });

  //    return {
  //      user,
  //      currentDate,
  //      isLoggedIn,
  //    };
  //  },
  };
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="app-title">
        <span class="icone"> 🔒 </span>  
        <span>Aplicação de apoio à Segurança</span>
      </div>
      <div class="usr_info">
        <router-link to="home">Home</router-link>
        <span> | </span>
        <router-link to="about">Sobre</router-link>
        <span> | </span>
        <router-link v-if="!isLoggedIn" to="http://localhost:8000/admin/login">Login</router-link>
        <router-link v-else to="http://localhost:8000/admin">
            {{ user }}
        </router-link>
        <span> | </span>
        <router-link v-if="isLoggedIn" to="http://localhost:8000/admin/logout">Logout | </router-link>
        <router-link  v-if="isLoggedIn" to="http://localhost:8000/admin/password_change">Trocar senha | </router-link>
        <span>Data/hora: {{ currentDate }}</span>
      </div>
    </header>
    <main class=app_main>
      <aside class="app-sidebar">
        <nav class="app-menu">
          <ul>
            <li class="menu_group" >
              <span class="menu_group_title">Administração</span>
              <ul>
                <li><router-link to="tipoaplicacao">Tipos de aplicação</router-link></li>
                <!--<li><router-link to="http://192.168.0.22/admin/password_change">Trocar senha</router-link></li>-->
              </ul>
            </li>
            <li>
              <span class="menu-group-title">Segurança das aplicações</span>
              <ul>
                <li>Aplicações</li>
                <li>Varreduras</li>
              </ul>
            </li>
          </ul>
        </nav>
      </aside>
      <div class="app-content">

        Mensagem no corpo da página
      </div>
    </main>
  </div>  
</template>

<style scoped>
  .icone {
    display:inline;
    align-items: center;
  }

  .app-container {
    display: flex;
    flex-direction: column;
    height: 90vh;
    width: 85vw;
    background-color: #ccffff;
  }

  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #004D4D;
    font-weight: bold;
    color: white;
  }

  .app-title {
    font-size: 25px;
    font-weight: bold;
  }

  .user-info {
    display: flex;
    align-items: center;
  }

  .app-main {
    display: flex;
    flex: 1;
  }

  .app-sidebar {
    width: 250px;
    background-color: #00b3b3;
    padding: 10px;
    color: white;
  }

  .app-menu {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .menu-group {
    margin-left: 10px;
    margin-bottom: 20px;
  }

  .menu-group-title {
    font-weight: bold;
    margin-left: 0px;
    margin-bottom: 10px;
    background-color: #205461;
  }

  .app-content {
    flex: 1;
    padding: 20px;
    color:black
  }
</style>
