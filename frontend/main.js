fetch(
"http://127.0.0.1:5000/recommend"
)


.then(
response=>response.json()
)


.then(
data=>{


let usersDiv=
document.getElementById(
"users"
);



data.similarUsers.forEach(
user=>{


usersDiv.innerHTML += `

<div class="card">

<h3>
${user.name}
</h3>


<p>
相似度:
${user.score*100}%
</p>


</div>

`;

}

);






let productDiv=
document.getElementById(
"products"
);



data.recommendProducts.forEach(
item=>{


productDiv.innerHTML +=`

<div class="product">

<h3>
${item.product}
</h3>

<p>
推荐理由:
${item.reason}
</p>


</div>


`;

}

);



}

);