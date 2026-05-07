Compare MaxSat and MIP for pathwidth
====================================

David Coudert ("A note on Integer Linear Programming formulations for
linear ordering problems on graphs") describes a number of different
MIP formulations for the minimum pathwidth problem on undirected
graphs. The one that we consider is the following: We are given an
unidirected graph $G = (V,E)$. Let $n=\#V$. We define the
following MIP. The binary variable $y_{v,t}$ is 1 if and only if the
vertex $v$ is placed in position $t$. The binary variable $u_{v,t}$ is
1 if and only if the vertex $v$ has a neighbor in position $>t$.

> Minimize $z$  
> Subject to:  
>   $\sum_{v \in V}\, y_{v,t} = t\text{ for }t=1,\dots,n$  
>   $y_{v,t} \le y_{v,t+1}\text{ for }v \in V, t=1,\dots,n-1$  
>   $y_{v,t} \le u_{v,t} + y_{w,t}\text{ for }(v,w) \in E, t=1,\dots,n$  
>   $\sum_{v \in V}\, u_{v,t} \le z\text{ for }t=1,\dots,n$  
>   $y_{v,t}, u_{v,t} \in \{0,1\}\text{ for }v \in V, t=1,\dots,n$  
