<script lang="ts">
  import ProjectSelector from './ProjectSelector.svelte';

  let isSubmitting = false;
  let submitError = '';
  let submitSuccess = '';

  type FieldErrors = {
    fullName?: string;
    email?: string;
    experienceLevel?: string;
    techStack?: string;
    selectedProjects?: string;
    duration?: string;
    confirmAvailability?: string;
  };
  let fieldErrors: FieldErrors = {};

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  type EmployeePayload = {
    id?: number;
    fullName: string;
    email: string;
    experienceLevel: string;
    techStack: string;
    selectedProjects: number[];
    duration: string;
    additionalSkills: string;
    confirmAvailability: boolean;
  };

  let formData: EmployeePayload = {
    fullName: '',
    email: '',
    experienceLevel: '',
    techStack: '',
    selectedProjects: [],
    duration: '',
    additionalSkills: '',
    confirmAvailability: false
  };

  function validateForm(): boolean {
    fieldErrors = {};
    let isValid = true;

    if (formData.fullName.trim() === '') {
      fieldErrors.fullName = 'Full Name is required';
      isValid = false;
    }

    if (formData.email.trim() === '') {
      fieldErrors.email = 'Email Address is required';
      isValid = false;
    } else if (!emailRegex.test(formData.email.trim())) {
      fieldErrors.email = 'Please enter a valid email address';
      isValid = false;
    }

    if (formData.experienceLevel === '') {
      fieldErrors.experienceLevel = 'Experience Level is required';
      isValid = false;
    }

    if (formData.techStack === '') {
      fieldErrors.techStack = 'Primary Technology Stack is required';
      isValid = false;
    }

    if (formData.selectedProjects.length === 0) {
      fieldErrors.selectedProjects = 'At least one project must be selected';
      isValid = false;
    }

    if (formData.duration === '') {
      fieldErrors.duration = 'Duration is required';
      isValid = false;
    }

    if (!formData.confirmAvailability) {
      fieldErrors.confirmAvailability = 'You must confirm availability';
      isValid = false;
    }

    return isValid;
  }

  function focusFirstError() {
    const order: Array<keyof FieldErrors | 'ps-toggle'> = [
      'fullName',
      'email',
      'experienceLevel',
      'techStack',
      'ps-toggle',
      'duration',
      'confirmAvailability'
    ];

    for (const id of order) {
      if (id === 'ps-toggle') {
        if (fieldErrors.selectedProjects) {
          const el = document.getElementById('ps-toggle') as HTMLElement | null;
          if (el && typeof el.focus === 'function') el.focus();
          break;
        }
        continue;
      }

      if (fieldErrors && fieldErrors[id]) {
        const el = document.getElementById(id) as HTMLElement | null;
        if (el && typeof el.focus === 'function') {
          el.focus();
        }
        break;
      }
    }
  }

  async function handleSubmit() {
    submitError = '';
    submitSuccess = '';

    if (!validateForm()) {
      submitError = 'Please fix the errors above';
      focusFirstError();
      return;
    }

    isSubmitting = true;
    try {
      const response = await fetch('http://127.0.0.1:5000/api/employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        const errBody = await response.json().catch(() => null);
        if (errBody?.details && typeof errBody.details === 'object') {
          fieldErrors = errBody.details;
          throw new Error(errBody.error || 'Please fix the errors above');
        }
        throw new Error(errBody?.error || 'Failed to submit form');
      }
      const savedResult = await response.json();
      if (savedResult?.employee) formData = savedResult.employee;
      submitSuccess = response.status === 201
        ? 'Profile created successfully!'
        : 'Profile updated successfully!';
    } catch (err) {
      submitError = err instanceof Error ? err.message : 'An unknown error occurred';
    } finally {
      isSubmitting = false;
    }
  }

  function handleClear() {
    formData = {
      fullName: '', email: '', experienceLevel: '', techStack: '',
      selectedProjects: [], duration: '', additionalSkills: '', confirmAvailability: false
    };
    submitError = '';
    submitSuccess = '';
  }

  let openExperience = false;
  let openTechStack = false;
  let openDuration = false;
</script>

<div class="form-wrapper">
  <header class="form-header">
    <h1>Project Assignment Form</h1>
    <p>Complete your profile to get assigned to internal projects.</p>
  </header>

  <form novalidate on:submit|preventDefault={handleSubmit}>

    <section>
      <h2><span class="section-num">01</span> Personal Information</h2>

      <div class="field">
        <label for="fullName">Full Name</label>
        <input id="fullName" type="text" bind:value={formData.fullName} placeholder="Your full name" />
        {#if fieldErrors.fullName}
          <span class="field-error">{fieldErrors.fullName}</span>
        {/if}
      </div>

      <div class="field">
        <label for="email">Email Address</label>
        <input id="email" type="email" bind:value={formData.email} placeholder="name@company.com" />
        {#if fieldErrors.email}
          <span class="field-error">{fieldErrors.email}</span>
        {/if}
      </div>
    </section>

    <section>
      <h2><span class="section-num">02</span> Experience &amp; Skills</h2>

      <div class="field">
        <label for="experienceLevel">Experience Level</label>
        <div class="select-wrap">
          <select id="experienceLevel" bind:value={formData.experienceLevel}
            on:mousedown={() => openExperience = !openExperience}
            on:change={() => openExperience = false}
            on:blur={() => openExperience = false}>
            <option value="">Select your level</option>
            <option value="junior">Junior (0–2 years)</option>
            <option value="mid">Mid-level (2–5 years)</option>
            <option value="senior">Senior (5+ years)</option>
          </select>
          <svg class="select-chevron" class:rotated={openExperience} width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 5l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        {#if fieldErrors.experienceLevel}
          <span class="field-error">{fieldErrors.experienceLevel}</span>
        {/if}
      </div>

      <div class="field">
        <label for="techStack">Primary Technology Stack</label>
        <div class="select-wrap">
          <select id="techStack" bind:value={formData.techStack}
            on:mousedown={() => openTechStack = !openTechStack}
            on:change={() => openTechStack = false}
            on:blur={() => openTechStack = false}>
            <option value="">Choose one</option>
            <option value="backend">Backend Development</option>
            <option value="frontend">Frontend Development</option>
            <option value="fullstack">Full-Stack Development</option>
            <option value="data">Data Engineering</option>
            <option value="devops">DevOps</option>
            <option value="mobile">Mobile Development</option>
          </select>
          <svg class="select-chevron" class:rotated={openTechStack} width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 5l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        {#if fieldErrors.techStack}
          <span class="field-error">{fieldErrors.techStack}</span>
        {/if}
      </div>

      <div class="field">
        <label for="additionalSkills">Additional Skills <span class="optional">(optional)</span></label>
        <input id="additionalSkills" type="text" placeholder="e.g., Python, Docker, React" bind:value={formData.additionalSkills} />
      </div>
    </section>

    <section>
      <h2><span class="section-num">03</span> Project Preferences</h2>

      <div class="field">
        <ProjectSelector bind:selectedProjects={formData.selectedProjects} />
        {#if fieldErrors.selectedProjects}
          <span class="field-error">{fieldErrors.selectedProjects}</span>
        {/if}
      </div>

      <div class="field">
        <label for="duration">Preferred Project Duration</label>
        <div class="select-wrap">
          <select id="duration" bind:value={formData.duration}
            on:mousedown={() => openDuration = !openDuration}
            on:change={() => openDuration = false}
            on:blur={() => openDuration = false}>
            <option value="">Select duration</option>
            <option value="short">Short-term (1–3 months)</option>
            <option value="medium">Medium-term (3–6 months)</option>
            <option value="long">Long-term (6+ months)</option>
          </select>
          <svg class="select-chevron" class:rotated={openDuration} width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M2 5l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>        {#if fieldErrors.duration}
          <span class="field-error">{fieldErrors.duration}</span>
        {/if}      </div>
    </section>

    <section>
      <h2><span class="section-num">04</span> Confirmation</h2>

      <div class="field">
        <label class="checkbox-label">
          <input type="checkbox" bind:checked={formData.confirmAvailability} />
          <span>I confirm my availability for the selected projects</span>
        </label>
        {#if fieldErrors.confirmAvailability}
          <span class="field-error">{fieldErrors.confirmAvailability}</span>
        {/if}
      </div>
    </section>

    <div class="actions">
      {#if submitError}
        <p class="msg msg--error">{submitError}</p>
      {/if}
      {#if submitSuccess}
        <p class="msg msg--success">{submitSuccess}</p>
      {/if}

      <button type="submit" class="btn-submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting…' : 'Submit Profile'}
      </button>

      <button type="button" class="btn-clear" on:click={handleClear}>Clear form</button>
    </div>
  </form>
</div>

<style>
  .form-wrapper {
    max-width: 720px;
    margin: 0 auto;
    font-family: var(--font-body);
    color: var(--text);
  }

  .form-header {
    margin-bottom: 56px;
    text-align: center;
  }

  .form-header h1 {
    font-family: var(--font-heading);
    font-size: 2rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
  }

  .form-header p {
    font-size: 1rem;
    color: var(--muted);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 72px;
  }

  section {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  section h2 {
    font-family: var(--font-heading);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }

  .section-num {
    font-family: var(--font-body);
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--muted);
    letter-spacing: 0.05em;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  label {
    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
  }

  .optional {
    font-family: var(--font-body);
    font-weight: 400;
    font-size: 0.8rem;
    color: var(--muted);
  }

  input[type="text"],
  input[type="email"],
  select {
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--text);
    background: var(--input-bg);
    border: 1.5px solid var(--border);
    border-radius: 4px;
    padding: 10px 36px 10px 12px;
    width: 100%;
    outline: none;
    transition: border-color 0s;
  }

  input[type="text"] {
    padding: 10px 12px;
  }
  input[type="email"] {
    padding: 10px 12px;
  }

  input[type="text"]:focus,
  input[type="email"]:focus,
  select:focus {
    border-color: var(--border-focus);
  }

  .select-wrap {
    position: relative;
    display: flex;
    align-items: center;
  }

  .select-wrap select {
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
  }

  .select-chevron {
    position: absolute;
    right: 12px;
    pointer-events: none;
    color: var(--muted);
    transition: transform 0.15s;
  }

  .select-chevron.rotated {
    transform: rotate(180deg);
    color: var(--accent);
  }

  .field:focus-within > label {
    color: var(--accent);
  }

  .checkbox-label {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    font-family: var(--font-body);
    font-size: 0.95rem;
    font-weight: 400;
    color: var(--text);
  }

  .checkbox-label input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--accent);
    flex-shrink: 0;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .btn-submit {
    font-family: var(--font-body);
    font-size: 0.95rem;
    font-weight: 500;
    color: #fff;
    background: var(--accent);
    border: none;
    border-radius: 4px;
    padding: 14px;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .btn-submit:disabled {
    background: #C8C8C4;
    cursor: not-allowed;
    opacity: 1;
  }

  .btn-submit:not(:disabled):hover {
    opacity: 0.88;
  }

  .btn-clear {
    background: none;
    border: none;
    color: var(--muted);
    font-family: var(--font-body);
    font-size: 0.85rem;
    cursor: pointer;
    text-decoration: underline;
    align-self: center;
    padding: 0;
  }

  .btn-clear:hover {
    color: var(--text);
  }

  .msg {
    font-size: 0.875rem;
    padding: 10px 14px;
    border-radius: 4px;
  }

  .msg--error {
    background: #fdf0ee;
    color: var(--error);
    border: 1px solid #e8b4ae;
  }

  .msg--success {
    background: #eef6f0;
    color: #1e6b3a;
    border: 1px solid #a8d5b5;
  }

  .field-error {
    font-size: 0.75rem;
    color: var(--error);
    font-family: var(--font-body);
  }
</style>