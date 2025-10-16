# app/repositories/member_transactions_accrual_repository.py
import sqlite3
from typing import Optional, Dict, Any
from app.models.MemberTransactionAccrual import MemberTransactionAccrual
from app.Database.context import DbContext


class MemberTransactionsAccrualRepository:
    def __init__(self):
        self.conn = DbContext.get_instance().get_connection()

    def save(self, txn: MemberTransactionAccrual) -> Optional[Dict[str, Any]]:
        """
        Guarda una transacción de acumulación de puntos en la base de datos.
        Retorna un diccionario con los datos insertados o None si hay error.
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO member_transactions_accrual (
                    hSponsorId,
                    hBitType,
                    hBitCategory,
                    hMemberId,
                    hBitDate,
                    hBitCurrency,
                    hBitAmount,
                    hBitSourceGeneratedId,
                    taxAmount,
                    processingDate,
                    pointsRewarded,
                    pointsRedeemed,
                    pointsReset,
                    status,
                    bitId,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                txn.hSponsorId,
                txn.hBitType,
                txn.hBitCategory,
                txn.hMemberId,
                txn.hBitDate,
                txn.hBitCurrency,
                txn.hBitAmount,
                txn.hBitSourceGeneratedId,
                txn.taxAmount,
                txn.processingDate,
                int(txn.pointsRewarded),
                int(txn.pointsRedeemed),
                int(txn.pointsReset),
                txn.status,
                txn.bitId,
                txn.created_at
            ))
            self.conn.commit()
            
            return {
                "id": cur.lastrowid,
                "bitId": txn.bitId,
                "hMemberId": txn.hMemberId,
                "hBitAmount": txn.hBitAmount,
                "hBitCurrency": txn.hBitCurrency,
                "processingDate": txn.processingDate,
                "status": txn.status
            }

        except sqlite3.IntegrityError as e:
            print(f"[DB ERROR] IntegrityError: {e}")
            return None
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None
