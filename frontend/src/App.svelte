<script lang="ts">
  import EmployeeForm from './lib/EmployeeForm.svelte'
</script>

<div class="page-shell">
  <header class="hero">
    <div class="hero__logo">
      <img src="/telia_logo_512.png" alt="Telia logo" width="28" height="28" />
    </div>
    <div class="hero__text">
      <h1>Telia Project Assignment Form</h1>
      <p>Complete your profile to get assigned to internal projects.</p>
    </div>
  </header>

  <section class="panel">
    <EmployeeForm />
  </section>
</div>
