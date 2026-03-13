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
  type FieldKey = keyof FieldErrors;
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

  function getFieldError(field: FieldKey): string | undefined {
    if (field === 'fullName' && formData.fullName.trim() === '') {
      return 'Full Name is required';
    }

    if (field === 'email') {
      const email = formData.email.trim();
      if (email === '') {
        return 'Email Address is required';
      }
      if (!emailRegex.test(email)) {
        return 'Please enter a valid email address';
      }
    }

    if (field === 'experienceLevel' && formData.experienceLevel === '') {
      return 'Experience Level is required';
    }

    if (field === 'techStack' && formData.techStack === '') {
      return 'Primary Technology Stack is required';
    }

    if (field === 'selectedProjects' && formData.selectedProjects.length === 0) {
      return 'At least one project must be selected';
    }

    if (field === 'duration' && formData.duration === '') {
      return 'Duration is required';
    }

    if (field === 'confirmAvailability' && !formData.confirmAvailability) {
      return 'Availability is required';
    }

    return undefined;
  }

  function validateField(field: FieldKey): boolean {
    const error = getFieldError(field);
    if (error) {
      fieldErrors = { ...fieldErrors, [field]: error };
      return false;
    }

    const nextErrors = { ...fieldErrors };
    delete nextErrors[field];
    fieldErrors = nextErrors;
    return true;
  }

  function validateIfInvalid(field: FieldKey) {
    if (fieldErrors[field]) {
      validateField(field);
    }
  }

  function isSubmitReady(): boolean {
    return (
      formData.fullName.trim() !== '' &&
      formData.email.trim() !== '' &&
      emailRegex.test(formData.email.trim()) &&
      formData.experienceLevel !== '' &&
      formData.techStack !== '' &&
      formData.selectedProjects.length > 0 &&
      formData.duration !== '' &&
      formData.confirmAvailability
    );
  }

  function validateForm(): boolean {
    const validationResults = [
      validateField('fullName'),
      validateField('email'),
      validateField('experienceLevel'),
      validateField('techStack'),
      validateField('selectedProjects'),
      validateField('duration'),
      validateField('confirmAvailability')
    ];

    return validationResults.every(Boolean);
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
      submitError = 'Make sure all fields are correctly filled out';
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
    fieldErrors = {};
    submitError = '';
    submitSuccess = '';
    openExperience = false;
    openTechStack = false;
    openDuration = false;
  }

  let openExperience = false;
  let openTechStack = false;
  let openDuration = false;
</script>

<div class="form-wrapper">
  <form novalidate on:submit|preventDefault={handleSubmit}>

    <section>
      <h2><span class="section-num">01</span> Personal Information</h2>

      <div class="field">
        <label for="fullName">Full Name *</label>
        <input
          id="fullName"
          type="text"
          bind:value={formData.fullName}
          placeholder="Your full name"
          on:blur={() => validateField('fullName')}
          on:input={() => validateIfInvalid('fullName')}
        />
        {#if fieldErrors.fullName}
          <span class="field-error">{fieldErrors.fullName}</span>
        {/if}
      </div>

      <div class="field">
        <label for="email">Email Address *</label>
        <input
          id="email"
          type="email"
          bind:value={formData.email}
          placeholder="name@company.com"
          on:blur={() => validateField('email')}
          on:input={() => validateIfInvalid('email')}
        />
        {#if fieldErrors.email}
          <span class="field-error">{fieldErrors.email}</span>
        {/if}
      </div>
    </section>

    <section>
      <h2><span class="section-num">02</span> Experience &amp; Skills</h2>

      <div class="field">
        <label for="experienceLevel">Experience Level *</label>
        <div class="select-wrap">
          <select id="experienceLevel" bind:value={formData.experienceLevel}
            on:mousedown={() => openExperience = !openExperience}
            on:change={() => { openExperience = false; validateField('experienceLevel'); }}
            on:blur={() => { openExperience = false; validateField('experienceLevel'); }}>
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
        <label for="techStack">Primary Technology Stack *</label>
        <div class="select-wrap">
          <select id="techStack" bind:value={formData.techStack}
            on:mousedown={() => openTechStack = !openTechStack}
            on:change={() => { openTechStack = false; validateField('techStack'); }}
            on:blur={() => { openTechStack = false; validateField('techStack'); }}>
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
        <ProjectSelector
          bind:selectedProjects={formData.selectedProjects}
          on:interact={() => validateField('selectedProjects')}
        />
        {#if fieldErrors.selectedProjects}
          <span class="field-error">{fieldErrors.selectedProjects}</span>
        {/if}
      </div>

      <div class="field">
        <label for="duration">Preferred Project Duration *</label>
        <div class="select-wrap">
          <select id="duration" bind:value={formData.duration}
            on:mousedown={() => openDuration = !openDuration}
            on:change={() => { openDuration = false; validateField('duration'); }}
            on:blur={() => { openDuration = false; validateField('duration'); }}>
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
          <input
            type="checkbox"
            bind:checked={formData.confirmAvailability}
            on:change={() => validateField('confirmAvailability')}
            on:blur={() => validateField('confirmAvailability')}
          />
          <span>I confirm my availability for the selected projects *</span>
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

      <button type="submit" class="btn-submit" disabled={isSubmitting || !isSubmitReady()}>
        {isSubmitting ? 'Submitting…' : 'Submit Profile'}
      </button>

      <button type="button" class="btn-clear" on:click={handleClear}>Clear form</button>
    </div>
  </form>
</div>

<style>
  .form-wrapper {
    max-width: 820px;
    margin: 0 auto;
    font-family: var(--font-body);
    color: var(--text);
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 48px;
  }

  section {
    display: flex;
    flex-direction: column;
    gap: 22px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 16px 20px;
    box-shadow: var(--shadow);
  }

  section h2 {
    font-family: var(--font-heading);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }

  .section-num {
    font-family: var(--font-body);
    font-size: 0.75rem;
    font-weight: 600;
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
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text);
  }

  .optional {
    font-family: var(--font-body);
    font-weight: 500;
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
    border-radius: var(--radius);
    padding: 12px 40px 12px 12px;
    width: 100%;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s, transform 0.1s ease;
  }

  input[type="text"],
  input[type="email"] { padding: 12px 12px; }

  input:focus,
  select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(108, 43, 217, 0.1);
    transform: translateY(-1px);
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

  .select-chevron.rotated { transform: rotate(180deg); color: var(--primary); }

  .field:focus-within > label { color: var(--primary); }

  .checkbox-label {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    font-family: var(--font-body);
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
  }

  .checkbox-label input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--primary);
    flex-shrink: 0;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .btn-submit {
    font-family: var(--font-body);
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    background: var(--primary);
    border: none;
    border-radius: var(--radius);
    padding: 14px;
    width: 100%;
    cursor: pointer;
    transition: transform 0.12s ease, box-shadow 0.2s;
    box-shadow: 0 14px 28px -22px rgba(83, 31, 179, 0.6);
  }

  .btn-submit:hover { transform: translateY(-1px); box-shadow: 0 16px 32px -24px rgba(83, 31, 179, 0.7); }

  .btn-submit:disabled {
    background: #d5c7f1;
    cursor: not-allowed;
    box-shadow: none;
  }

  .btn-clear {
    background: none;
    border: none;
    color: var(--muted);
    font-family: var(--font-body);
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    text-decoration: underline;
    align-self: flex-start;
    padding: 0;
  }

  .btn-clear:hover { color: var(--text); }

  .msg {
    font-size: 0.9rem;
    padding: 12px 14px;
    border-radius: 10px;
    font-weight: 700;
  }

  .msg--error {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
  }

  .msg--success {
    background: #ECFDF3;
    color: #166534;
    border: 1px solid #BBF7D0;
  }

  .field-error {
    font-size: 0.8rem;
    color: var(--error);
    font-family: var(--font-body);
    font-weight: 600;
  }
</style>