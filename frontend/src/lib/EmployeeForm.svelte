<script>
  let formData = {
    fullName: '',
    email: '',
    experienceLevel: '',
    techStack: '',
    selectedProjects: [],
    duration: '',
    additionalSkills: '',
    confirmAvailability: false
  };

  function handleSubmit() {
    console.log('Form submitted:', formData);
    // TODO: Send to Flask backend
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
    <input type="text" bind:value={formData.fullName} required />
  </label>

  <label>
    Email Address:
    <input type="email" bind:value={formData.email} required />
  </label>

  <label>
    Experience Level:
    <select bind:value={formData.experienceLevel} required>
      <option value="">Select your level</option>
      <option value="junior">Junior (0-2 years)</option>
      <option value="mid">Mid-level (2-5 years)</option>
      <option value="senior">Senior (5+ years)</option>
    </select>
  </label>

  <label>
    Primary Technology Stack:
    <select bind:value={formData.techStack} required>
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
    Available Projects:
    <select multiple size="8" bind:value={formData.selectedProjects} required>
      <option value="1">Customer Portal Redesign</option>
      <option value="2">Data Pipeline Migration</option>
      <option value="3">Mobile App Enhancement</option>
      <option value="4">Internal Analytics Dashboard</option>
      <option value="5">API Gateway Implementation</option>
      <option value="6">Cloud Infrastructure Setup</option>
      <option value="7">E-commerce Platform Update</option>
      <option value="8">Reporting System Automation</option>
      <option value="9">Microservices Architecture Transition</option>
      <option value="10">Customer Data Platform Integration</option>
    </select>
  </label>

  <fieldset>
    <legend>Preferred Project Duration:</legend>
    <label>
      <input type="radio" value="short" bind:group={formData.duration} required />
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
    <input type="checkbox" bind:checked={formData.confirmAvailability} required />
    I confirm my availability for the selected projects
  </label>

  <button type="submit">Save Profile</button>
  <button type="button" on:click={handleClear}>Clear Form</button>
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