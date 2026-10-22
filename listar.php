<?php
header('Content-Type: text/html; charset=utf-8');
include 'conexao.php';
$res = $conn->query("SELECT * FROM mensagens");
?>

<a href="../pages/contato.html">Voltar para Contato</a><br><br>

<table border="1">
    <tr>
        <th>ID</th>
        <th>Nome</th>
        <th>E-mail</th>
        <th>Mensagem</th>
        <th>Ações</th>
    </tr>
    <?php while($row = $res->fetch_assoc()): ?>
    <tr>
        <td><?= $row['id'] ?></td>
        <td><?= $row['nome'] ?></td>
        <td><?= $row['email'] ?></td>
        <td><?= $row['mensagem'] ?></td>
        <td>
            <a href="editar.php?id=<?= $row['id'] ?>">Editar</a> | 
            <a href="excluir.php?id=<?= $row['id'] ?>">Excluir</a>
        </td>
    </tr>
    <?php endwhile; ?>
</table>