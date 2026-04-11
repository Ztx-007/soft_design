原生代码强耦合 见before_api

router里面，挂了一条route
功能和数据库，直接强实现在业务代码里面，如果更换数据库或换个业务逻辑 很难维护
看看新的port And adapters实现 这种方法反向解耦 port只提供要实现什么 可以随时更换适配器adapters




