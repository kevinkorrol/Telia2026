<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { onMount } from 'svelte';
  import { clickOutside } from './actions';

  export let selectedProjects: number[] = [];

  let projects: Array<{ id: number; name: string }> = [];
  let loading = true;
  let error = '';
  let isOpen = false;
  const dispatch = createEventDispatcher();

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
    selectedProjects = selectedProjects.includes(projectId)
      ? selectedProjects.filter(id => id !== projectId)
      : [...selectedProjects, projectId];
    dispatch('interact');
  }

  function getSelectedNames(): string {
    if (selectedProjects.length === 0) return 'Select projects…';
    return projects
      .filter(p => selectedProjects.includes(p.id))
      .map(p => p.name)
      .join(', ');
  }

  onMount(() => {
    loadProjects();
  });
</script>

<div
  class="ps-wrapper"
  use:clickOutside={() => {
    if (isOpen) {
      isOpen = false;
      dispatch('interact');
    }
  }}
>
  <label class="ps-label" for="ps-toggle">Available Projects *</label>
  {#if loading}
    <p class="ps-state">Loading…</p>
  {:else if error}
    <p class="ps-state ps-state--error">{error}</p>
  {:else}
    <div class="ps-dropdown" class:is-open={isOpen}>
      <button
        id="ps-toggle"
        type="button"
        class="ps-toggle"
        on:click={() => {
          isOpen = !isOpen;
          if (!isOpen) {
            dispatch('interact');
          }
        }}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span class="ps-toggle-text" class:placeholder={selectedProjects.length === 0}>{getSelectedNames()}</span>
        <svg class="ps-chevron" class:rotated={isOpen} width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2 5l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      {#if isOpen}
        <div class="ps-menu" role="listbox" aria-multiselectable="true">
          {#each projects as project}
            <label class="ps-item">
              <input
                type="checkbox"
                checked={selectedProjects.includes(project.id)}
                on:change={() => toggleProject(project.id)}
              />
              {project.name}
            </label>
          {/each}
        </div>
      {/if}
    </div>

    {#if !isOpen && selectedProjects.length > 0}
      <div class="ps-chips">
        {#each projects.filter(p => selectedProjects.includes(p.id)) as project}
          <span class="ps-chip">
            {project.name}
            <button
              type="button"
              class="ps-chip-remove"
              aria-label="Remove {project.name}"
              on:click={() => toggleProject(project.id)}
            >✕</button>
          </span>
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .ps-wrapper {
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
  }

  .ps-label {
    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text);
  }

  .ps-wrapper:focus-within .ps-label { color: var(--primary); }

  .ps-state {
    font-size: 0.9rem;
    color: var(--muted);
  }

  .ps-state--error {
    color: var(--error);
  }

  .ps-dropdown {
    position: relative;
    width: 100%;
  }

  .ps-toggle {
    width: 100%;
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--text);
    background: var(--input-bg);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 12px;
    text-align: left;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s, transform 0.1s ease;
  }

  .ps-dropdown.is-open .ps-toggle,
  .ps-toggle:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(108, 43, 217, 0.1);
    transform: translateY(-1px);
  }

  .ps-toggle-text {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--text);
  }

  .ps-toggle-text.placeholder {
    color: var(--muted);
  }

  .ps-chevron {
    flex-shrink: 0;
    color: var(--muted);
    transition: transform 0.15s;
  }

  .ps-chevron.rotated {
    transform: rotate(180deg);
  }

  .ps-menu {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    background: var(--input-bg);
    border: 1.5px solid var(--primary);
    border-radius: var(--radius);
    max-height: 260px;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 0 10px 28px -18px rgba(83, 31, 179, 0.25);
  }

  .ps-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    font-family: var(--font-body);
    font-size: 0.9rem;
    color: var(--text);
    cursor: pointer;
    border-bottom: 1px solid var(--border);
  }

  .ps-item:last-child {
    border-bottom: none;
  }

  .ps-item:hover { background: var(--item-hover-bg); }

  .ps-item input[type='checkbox'] {
    accent-color: var(--primary);
    width: 15px;
    height: 15px;
    flex-shrink: 0;
  }

  .ps-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
  }

  .ps-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--chip-bg);
    color: var(--primary-strong);
    border: 1px solid var(--chip-border);
    border-radius: 999px;
    padding: 4px 10px 4px 12px;
    font-family: var(--font-body);
    font-size: 0.8rem;
    font-weight: 600;
  }

  .ps-chip-remove {
    background: none;
    border: none;
    color: var(--primary-strong);
    cursor: pointer;
    font-size: 0.7rem;
    padding: 0;
    line-height: 1;
    opacity: 0.7;
  }

  .ps-chip-remove:hover {
    opacity: 1;
  }
</style>