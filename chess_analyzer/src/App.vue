<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">
            <div class="row">
                <div class="col">
                    <img
                        src="./assets/new_logo.svg"
                        class="logo d-inline-block"
                        alt="ChessAnalysisTool logo"
                    />
                </div>
                <div
                    class="col d-flex justify-content-center align-items-center"
                >
                    <p style="color: #1f3473">BishUp - Chess Analysis Tool</p>
                </div>
            </div>
        </a>
        <div>
            <ul class="navbar-nav"></ul>
        </div>
    </nav>
    <router-view />
</template>

<style scoped>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}
.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
