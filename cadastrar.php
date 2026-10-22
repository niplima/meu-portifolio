<?php
include 'conexao.php';

if ($_POST) {
    $conn->query("INSERT INTO mensagens (nome, email, mensagem) VALUES ('{$_POST['nome']}', '{$_POST['email']}', '{$_POST['mensagem']}')");
    header("Location: listar.php");
}
?>