define(function (require) {
    let Vue = require('vue');

    let template = '<span>Hols</span>';

    Vue.component('target', {
        props: ['destination'],
        template: template,
    });
});
