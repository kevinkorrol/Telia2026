<script lang="ts">
  import ProjectSelector from './ProjectSelector.svelte';
  let isSubmitting = false;
  let submitError = '';
  let submitSuccess = '';

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

  async function handleSubmit() {
    submitError = '';
    submitSuccess = '';
    isSubmitting = true;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/employees", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"},
            body:JSON.stringify(formData)
        });

        if (!response.ok){
            const errBody = await response.json().catch(() => null);
            throw new Error(errBody?.error || 'Failed to submit form');
        }

        const savedResult = await response.json();
        if (savedResult?.employee) {
          formData = savedResult.employee;
        }

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
      fullName: '',
      email: '',
      experienceLevel: '',
      techStack: '',
      selectedProjects: [],
      duration: '',
      additionalSkills: '',
      confirmAvailability: false
    };
  }
</script>

<h2>Project Assignment Form</h2>
<p>Complete your profile to get assigned to internal projects.</p>

<form on:submit|preventDefault={handleSubmit}>
  <label>
    Full Name:
    <input type="text" bind:value={formData.fullName}/>
  </label>

  <label>
    Email Address:
    <input type="email" bind:value={formData.email}/>
  </label>

  <label>
    Experience Level:
    <select bind:value={formData.experienceLevel}>
      <option value="">Select your level</option>
      <option value="junior">Junior (0-2 years)</option>
      <option value="mid">Mid-level (2-5 years)</option>
      <option value="senior">Senior (5+ years)</option>
    </select>
  </label>

  <label>
    Primary Technology Stack:
    <select bind:value={formData.techStack}>
      <option value="">Choose one</option>
      <option value="backend">Backend Development</option>
      <option value="frontend">Frontend Development</option>
      <option value="fullstack">Full-Stack Development</option>
      <option value="data">Data Engineering</option>
      <option value="devops">DevOps</option>
      <option value="mobile">Mobile Development</option>
    </select>
  </label>

  <label>
    <ProjectSelector bind:selectedProjects={formData.selectedProjects}/>
  </label>

  <fieldset>
    <legend>Preferred Project Duration:</legend>
    <label>
      <input type="radio" value="short" bind:group={formData.duration} />
      Short-term (1-3 months)
    </label>
    <label>
      <input type="radio" value="medium" bind:group={formData.duration} />
      Medium-term (3-6 months)
    </label>
    <label>
      <input type="radio" value="long" bind:group={formData.duration} />
      Long-term (6+ months)
    </label>
  </fieldset>

  <label>
    Additional Skills (optional):
    <input type="text" placeholder="e.g., Python, Docker, React" bind:value={formData.additionalSkills} />
  </label>

  <label>
    <input type="checkbox" bind:checked={formData.confirmAvailability} />
    I confirm my availability for the selected projects
  </label>

  <button type="submit" disabled={isSubmitting}>
    {isSubmitting ? 'Submitting...' : 'Submit'}
  </button>
  <button type="button" on:click={handleClear}>Clear Form</button>

  {#if submitError}
    <p style="color: red;">{submitError}</p>
  {/if}
  {#if submitSuccess}
    <p style="color: green;">{submitSuccess}</p>
  {/if}
</form>

<style>
  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 500px;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  fieldset {
    border: none;
    padding: 0;
  }

  legend {
    margin-bottom: 0.5rem;
  }

  button {
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
</style>