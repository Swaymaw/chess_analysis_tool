<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light py-2">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center gap-2" href="/">
                <img
                    src="./assets/new_logo.svg"
                    class="ml-2"
                    alt="ChessAnalysisTool logo"
                    style="height: 32px"
                />
                <span class="fw-semibold" style="color: #1f3473"
                    >BishUp – Chess Analysis Tool</span
                >
            </a>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#mainNavbar"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/analysis">Analysis</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <router-view />
</template>
