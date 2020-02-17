import React from "react";
import { Button, Icon, Table } from "semantic-ui-react";
import { stringToHex } from "../services";

export default function Transaction({ transaction, setTransaction }) {
  return (
    <div>
      <Button icon onClick={() => setTransaction()}>
        <Icon name="arrow left" />
      </Button>
      <Table celled>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Key</Table.HeaderCell>
            <Table.HeaderCell>Value</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          {Object.keys(transaction).map(t_k => (
            <Table.Row>
              <Table.Cell>{t_k}</Table.Cell>
              <Table.Cell>
                {t_k === "sig" && (
                  <div className="clbc-transaction-table-value">
                    {stringToHex(transaction[t_k])}
                  </div>
                )}
                {t_k === "ref" && "None"}
                {t_k === "frm" && "None"}
                {t_k === "amt" && transaction[t_k]}
                {t_k === "val" && "" + transaction[t_k]}
                {t_k === "snd" && (
                  <div className="clbc-transaction-table-value">
                    {transaction[t_k]}
                  </div>
                )}
                {t_k === "rcv" && (
                  <div className="clbc-transaction-table-value">
                    {transaction[t_k]}
                  </div>
                )}
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  );
}
