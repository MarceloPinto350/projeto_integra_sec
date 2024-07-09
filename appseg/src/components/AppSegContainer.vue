<template>
    <div class="app-container">
        
        <i>
            <slot name="logo"></slot>
        </i>
        <div class="tituto">
            <h1>
                <slot name="nome">Administração da AppSeg</slot>
            </h1>
        </div>
        <div class="ferramentas">
            <m>
                <slot name="ferramentas">
                    <a href="http://192.168.0.22:8000/admin/">admin</a> | 
                    <a href="http://192.168.0.22:8000/admin/logout/">Sair</a> |
                    Data e hora: 
                </slot>
            </m>
        </div>
    </div>    
</template>

  
<style scoped>
   .appheader {
        margin-top: 0.1rem;
        background-color: #5F9EA0;
    }

    i {
        display: flex;
        place-items: top;
        place-content: top;
        width: 16px;
        height: 16px;
        color: var(--color-text);
    }
  
    h1 {
        font-size: 2rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
        color: var(--color-heading);
    }
  
    .titulo {
        flex: 1;
        margin-left: 1rem;
    }

    m {
        flex: 1;
        margin-left: 1rem;
        align-items: padding-right;
    }
   
</style>
  