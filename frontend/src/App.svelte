<script lang="ts">
  import { onMount } from 'svelte'
  import EmployeeForm from './lib/EmployeeForm.svelte'

  const THEME_STORAGE_KEY = 'theme-mode'
  let isDarkMode = false

  function applyTheme() {
    document.documentElement.dataset.theme = isDarkMode ? 'dark' : 'light'
  }

  function toggleTheme() {
    isDarkMode = !isDarkMode
    applyTheme()
    localStorage.setItem(THEME_STORAGE_KEY, isDarkMode ? 'dark' : 'light')
  }

  onMount(() => {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY)
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkMode = savedTheme ? savedTheme === 'dark' : prefersDark
    applyTheme()
  })
</script>

<div class="page-shell">
  <header class="hero">
    <div class="hero__intro">
      <div class="hero__logo">
        <img src="/telia_logo_512.png" alt="Telia logo" width="28" height="28" />
      </div>
      <div class="hero__text">
        <h1>Telia Project Assignment Form</h1>
        <p>Complete your profile to get assigned to internal projects.</p>
      </div>
    </div>

    <button type="button" class="theme-toggle" on:click={toggleTheme}>
      {isDarkMode ? 'Light mode' : 'Dark mode'}
    </button>
  </header>

  <section class="panel">
    <EmployeeForm />
  </section>
</div>
