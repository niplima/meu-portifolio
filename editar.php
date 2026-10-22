<?php
header('Content-Type: text/html; charset=utf-8');
include 'conexao.php';
$id = $_GET['id'];

if ($_POST) {
    $conn->query("UPDATE mensagens SET nome='{$_POST['nome']}', email='{$_POST['email']}', mensagem='{$_POST['mensagem']}' WHERE id=$id");
    header("Location: listar.php");
}

$row = $conn->query("SELECT * FROM mensagens WHERE id=$id")->fetch_assoc();
?>

<form method="POST">
    Nome: <input type="text" name="nome" value="<?= $row['nome'] ?>" required><br><br>
    E-mail: <input type="email" name="email" value="<?= $row['email'] ?>" required><br><br>
    Mensagem: <textarea name="mensagem" required><?= $row['mensagem'] ?></textarea><br><br>
    <button type="submit">Salvar Alteração</button>
</form>