module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    'airbnb-base',
    'plugin:import/typescript',
  ],
  parserOptions: {
    ecmaVersion: 13,
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: [
    'vue',
    '@typescript-eslint',
  ],
  rules: {
    'vue/multi-word-component-names': ['off'],
    'linebreak-style': ['off'],
    'no-undef': ['off'],
    'import/extensions': ['error', 'ignorePackages', { ts: 'never' }],
    'max-len': ['off'],
    'no-param-reassign': ['error', { props: false }],
    'vue/max-len': ['error', { code: 120, template: 5000 }],
    'vue/no-multiple-template-root': ['off'],
    'no-plusplus': ['error', { allowForLoopAfterthoughts: true }],
  },
};
