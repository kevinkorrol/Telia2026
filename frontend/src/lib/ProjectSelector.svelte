<script lang="ts">
  export let selectedProjects: number[] = [];
  
  let projects: Array<{ id: number; name: string }> = [];
  let loading = true;
  let error = '';
  let isOpen = false;
  
  async function loadProjects() {
    try {
      const response = await fetch('http://localhost:5000/api/projects');
      if (!response.ok) throw new Error('Failed to fetch projects');
      projects = await response.json();
    } catch (err) {
      error = err instanceof Error ? err.message : 'An unknown error occurred';
    } finally {
      loading = false;
    }
  }
  
  function toggleProject(projectId: number) {
    if (selectedProjects.includes(projectId)) {
      selectedProjects = selectedProjects.filter(id => id !== projectId);
    } else {
      selectedProjects = [...selectedProjects, projectId];
    }
  }
  
  function getSelectedNames(): string {
    if (selectedProjects.length === 0) return 'Select projects...';
    return projects
      .filter(p => selectedProjects.includes(p.id))
      .map(p => p.name)
      .join(', ');
  }
  
  loadProjects();
</script>

<div class="project-selector">
  <p class="field-label">Available Projects:</p>
  {#if loading}
    <p>Loading projects...</p>
  {:else if error}
    <p style="color: red;">{error}</p>
  {:else}
    <div class="dropdown">
      <button type="button" class="dropdown-toggle" on:click={() => isOpen = !isOpen}>
        {getSelectedNames()}
        <span class="arrow">{isOpen ? '▲' : '▼'}</span>
      </button>
      
      {#if isOpen}
        <div class="dropdown-menu">
          {#each projects as project}
            <label class="dropdown-item">
              <input
                type="checkbox"
                value={project.id}
                checked={selectedProjects.includes(project.id)}
                on:change={() => toggleProject(project.id)}
              />
              {project.name}
            </label>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .project-selector {
    position: relative;
    margin: 1rem 0;
  }

  .field-label {
    margin: 0 0 0.5rem 0;
  }

  .dropdown {
    position: relative;
    width: 100%;
  }

  .dropdown-toggle {
    width: 100%;
    padding: 0.5rem;
    text-align: left;
    background: #424141;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .arrow {
    margin-left: 0.5rem;
  }

  .dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    max-height: 300px;
    overflow-y: auto;
    background: #424141;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 0.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }

  .dropdown-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    cursor: pointer;
    border-bottom: 1px solid #f0f0f0;
  }

  .dropdown-item:hover {
    background: #585656;
  }

  .dropdown-item:last-child {
    border-bottom: none;
  }

  .dropdown-item input[type="checkbox"] {
    margin-right: 0.5rem;
  }
</style>