export function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

export function debounceAsync(func, delay) {
  let timeout;

  return async function (...args) {
    clearTimeout(timeout);
    return new Promise((resolve, reject) => {
      timeout = setTimeout(async () => {
        try {
          const result = await func.apply(this, args);
          resolve(result);
        } catch (err) {
          reject(err);
        }
      }, delay);
    });
  };
}
