<script>
  import { ref, computed } from 'vue';
  //import { useDateTime } from '@/composables/useDateTime';
  //import { getCurrentUser } from '@/services/user';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const router = useRouter();
      const user = ref(null);
      const currentDate = computed(() => useDateTime());
      const isLoggedIn = computed(() => user.value !== null);

      getCurrentUser().then((userData) => {
        user.value = userData.name;
      });

      return {
        user,
        currentDate,
        isLoggedIn,
      };
    },
  };
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <i>
        <slot name="logo">IMG</slot>
      </i>
      <div class="app-title">Aplicação de apoio à Segurança</div>
      <div class="usr_info">
        <router-link v-if="!isLoggedIn" to="http://192.168.0.22/admin/login">Login</router-link>
          <router-link v-else to="/admin">
            {{ user }}
          </router-link>
          <span>|</span>
          <router-link v-if="isLoggedIn" to="/admin/logout">Logout</router-link>
          <span>|</span>
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
                <li><router-link to="http://192.168.0.22/admin">Administração - Default</router-link></li>
                <li><router-link to="http://192.168.0.22/admin/password_change">Trocar senha</router-link></li>
              </ul>
            </li>
            <li>
              <span class="menu-group-title">Segurança das aplicações</span>
              <ul>
                <li><router-link to="/applications">Aplicações</router-link></li>
                <li><router-link to="/scans">Varreduras</router-link></li>
              </ul>
            </li>
          </ul>
        </nav>
      </aside>
      <section class="app-content">
        <router-view />
      </section>
    </main>
  </div>  
</template>

<style scoped>
  .app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #f0f0f0;
  }

  .app-title {
    font-size: 20px;
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
    background-color: #f7f7f7;
    padding: 20px;
  }

  .app-menu {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .menu-group {
    margin-bottom: 20px;
  }

  .menu-group-title {
    font-weight: bold;
    margin-bottom: 10px;
  }

  .app-content {
    flex: 1;
    padding: 20px;
  }
</style>
