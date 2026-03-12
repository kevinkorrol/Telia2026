/**
 * Action to execute a callback when a click is detected outside of the node.
 * @param {HTMLElement} node The node to monitor for outside clicks.
 * @param {() => void} callback The function to call when an outside click is detected.
 */
export function clickOutside(node: HTMLElement, callback: () => void) {
  const handleClick = (event: MouseEvent) => {
    if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
      callback();
    }
  };

  document.addEventListener('mousedown', handleClick, true);

  return {
    destroy() {
      document.removeEventListener('mousedown', handleClick, true);
    }
  };
}
