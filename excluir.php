<?php
include 'conexao.php';
$conn->query("DELETE FROM mensagens WHERE id={$_GET['id']}");
header("Location: listar.php");
?>